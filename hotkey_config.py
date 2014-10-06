#-*-encoding=utf-8-*-

import keyboard 
#示例
CONFIG = (
        ((keyboard.LEFTCTRL, keyboard.NUM_0), 'firefox --private-window'),
        ((keyboard.LEFTCTRL, keyboard.NUM_9), 'nautilus'),
        ((keyboard.LEFTCTRL, keyboard.NUM_8), 'konsole'),
        ((keyboard.LEFTCTRL, keyboard.NUM_7), 'libreoffice --writer')
        ) 

#输出调试信息
DUMP = False

#后台执行
DAEMON = True

#日志
LOG = "/tmp/hotkeys.log"

#PID文件
PID = "/tmp/hotkeys.pid" 

#以某个用户执行命令
USER = "richard" 
