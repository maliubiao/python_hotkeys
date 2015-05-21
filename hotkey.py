#! /usr/bin/env python
#-*-encoding=utf-8-*-

import keyboard 
import select
import os
import sys
import pwd
import fcntl
import signal
import os.path
import hashlib
import stat

def run_as_user(user):
    try:
        db = pwd.getpwnam(user)
    except KeyError:
        raise Exception("user doesn't exists") 
    try:
        os.setgid(db.pw_gid)
    except OSError:        
        raise Exception("change gid failed") 
    try:
        os.setuid(db.pw_uid)
    except OSError:
        raise Exception("change uid failed") 

def find_kbds(): 
    f = open("/proc/bus/input/devices", "r")
    x = f.read().split("\n\n") 
    f.close()
    f = [] 
    for i in x: 
        for j in i.split("\n"):
            if j.startswith("B: LED="):
                f.append(i)
                break
    r = [] 
    for i in f:  
        if DUMP:
            print i
        s = i.find("H: Handlers=")
        if s < 0:
            raise OSError("find keyboard failed")
        s1 = i.find("\n", s)
        if s1 < 0:
            raise OSError("find keyboard failed")
        t = i[s:s1] 
        if not ("event" in t and "kbd" in t):
            continue 
        for k in t.split(" "):
            if k.startswith("event"):
                r.append(k)
                break 
    return ["/dev/input/"+x for x in r] 


def keys_hash(keys):
    return hashlib.md5("".join([chr(x).zfill(3) for x in sorted(keys)])).digest()


def keys_table(CONFIG):
    ret = {}
    for k,v in CONFIG:
        ret[keys_hash(k)] = v
    return ret


def poll(pollobj, fobj, pressed_now, nsec): 
    for fd, event in pollobj.poll(nsec): 
        #make sure no zombies
        try:
            os.wait3(os.WNOHANG)
        except OSError:
            pass
        if event & select.EPOLLIN:
            n = keyboard.parse_event(fobj)
            if DUMP:  
                d = n.copy()
                d["code"] = keyboard.key_table[n["code"]]
                d["type"] = keyboard.ev_table[n["type"]] 
                print d 
            if n["type"] == keyboard.EV_KEY: 
                if n["value"] >= keyboard.PRESSED:
                    pressed_now[n["code"]] = n["tv_sec"]
                elif n["value"] == keyboard.RELEASED:
                    if n["code"] in pressed_now:
                        del pressed_now[n["code"]] 
            if not pressed_now:
                continue
            keys = sorted(pressed_now.keys())
            h = keys_hash(keys)
            if h in KEYS_TABLE:
                action = KEYS_TABLE[h]
                #run as daemon
                if not os.fork(): 
                    os.setsid()
                    if not os.fork():
                        print "run:", action
                        os.execvp("/bin/sh", ["sh", "-c", action]) 
                    os.wait()
                    exit(0)
                #trigger once
                for k in keys:
                    del pressed_now[k] 
        if event & select.EPOLLERR: 
            exit(1) 

def run_listener(device): 
    pressed_now = {}
    f = open(device, "r") 
    x = select.epoll() 
    x.register(f.fileno(), select.EPOLLIN|select.EPOLLERR) 
    #drop privilege
    fcntl.fcntl(f.fileno(), fcntl.F_SETFD, fcntl.FD_CLOEXEC) 
    fcntl.fcntl(x.fileno(), fcntl.F_SETFD, fcntl.FD_CLOEXEC) 
    run_as_user(USER) 
    #reset environ
    home = pwd.getpwnam(USER).pw_dir
    os.environ["HOME"] = home
    os.environ["DISPLAY"] = ":0.0"
    os.environ["XAUTHORITY"] = home + "/.Xauthority" 
    while True:
        try:
            poll(x, f, pressed_now, 1)
        except IOError as e:
            pass

def bgrun():
    log_file = open(LOG, "w+", buffering=False)
    pid_file = open(PID, "w+", buffering=False) 
    fcntl.fcntl(log_file.fileno(), fcntl.F_SETFD, fcntl.FD_CLOEXEC) 
    fcntl.fcntl(pid_file.fileno(), fcntl.F_SETFD, fcntl.FD_CLOEXEC) 
    user = pwd.getpwnam(USER)
    os.chown(LOG, user.pw_uid, user.pw_gid)
    os.chown(PID, user.pw_uid, user.pw_gid)
    try:
        status = os.fork()
    except OSError as e:
        print e
    if not status:
        os.setsid() 
        stdin = open("/dev/null", "r")
        os.dup2(stdin.fileno(), 0)
        os.dup2(log_file.fileno(), 1)
        os.dup2(log_file.fileno(), 2) 
        try:
            status2 = os.fork()
        except OSError as e:
            print e
        if status2: 
            pid_file.write(str(status2))
            pid_file.close()
            exit() 
    else:
        exit() 

def hotkey(kbds): 
    table = {}
    for i in kbds:
        print "keyboard: ", i
        pid = os.fork()
        if not pid: 
            run_listener(i)
            exit(0) 
        table[pid] = i
    def force_quit(*args):
        for i in table:
            try:
                os.kill(i, signal.SIGKILL)
            except OSError:
                pass
        try:
            os.remove(PID)
        except OSError:
            pass
    signal.signal(signal.SIGINT, force_quit) 
    #make sure no zombies 
    run_as_user(USER)
    while True:
        try:
            pid, _ = os.wait()
            print "die :", table[pid]
        except OSError: 
            exit(0) 
        except KeyboardInterrupt:
            print "die" 
            exit(0) 

def pid_exists(pid):
    if not os.access(pid, os.F_OK):
        return False
    f = open(pid, "r")
    pid = int(f.read())
    f.close()
    return os.access("/proc/%d % pid", os.F_OK) and "hotkey.py" in open("/proc/%d/cmdline" % pid).read()

if __name__ == "__main__": 
    from hotkey_config import CONFIG, DUMP, USER, DAEMON, LOG, PID 
    if pid_exists(PID):
        print "already running"
        exit(0) 
    if DAEMON: 
        print "log: ", LOG
        print "pid: ", PID
        bgrun()
    KEYS_TABLE = keys_table(CONFIG) 
    hotkey(find_kbds()) 
