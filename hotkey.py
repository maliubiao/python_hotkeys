import keyboard 

import select
import os
import pwd
import fcntl
import os.path


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
        for fd, event in x.poll(1): 
            #make sure no zombies
            try:
                os.wait3(os.WNOHANG)
            except OSError:
                pass
            if event & select.EPOLLIN:
                n = keyboard.parse_event(f)
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
                for key in CONFIG:
                    ks, action = key
                    if all([k in pressed_now for k in ks]): 
                        #run as daemon
                        if not os.fork(): 
                            os.setsid()
                            if not os.fork():
                                print "run:", action
                                os.execvp("/bin/sh", ["sh", "-c", action]) 
                            os.wait()
                            exit(0)
                        #trigger once
                        for k in ks:
                            del pressed_now[k]
                        #pressed_now = {}
            if event & select.EPOLLERR: 
                exit(1) 

def hotkey(kbds): 
    #open keyboard 
    table = {}
    for i in kbds:
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
    from hotkey_config import CONFIG, DUMP, USER 
    hotkey(find_kbds()) 
