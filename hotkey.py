import keyboard 

import select
import os
import pwd
import fcntl
import signal
import os.path
import hashlib

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
    os.environ["XAUTHORITY"] = home + "/.Xauthority" 
    while True:
        try:
            poll(x, f, pressed_now, 1)
        except IOError as e:
            pass

def hotkey(kbds): 
    #open keyboard 
    table = {}
    for i in kbds:
        print "kbd: ", i
        pid = os.fork()
        if not pid: 
            run_listener(i)
            exit(0) 
        table[pid] = i
    #make sure no zombies 
    while True:
        try:
            pid, _ = os.wait()
            print "die :", table[pid]
        except OSError: 
            exit(0) 
        except KeyboardInterrupt:
            print "die" 
            exit(0) 


if __name__ == "__main__":
    import pdb
    from hotkey_config import CONFIG, DUMP, USER 
    KEYS_TABLE = keys_table(CONFIG) 
    hotkey(find_kbds()) 
