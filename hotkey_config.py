#-*-encoding=utf-8-*-

import keyboard 
#示例
CONFIG = (
        ((keyboard.LEFTCTRL, keyboard.LEFTALT, keyboard.NUM_0), 'echo hello 1'),
        ((keyboard.LEFTCTRL, keyboard.NUM_9), 'echo hello 2'),
        ((keyboard.LEFTCTRL, keyboard.M), 'echo hello 3')
        ) 

#输出调试信息
DUMP = False

#以某个用户执行命令
USER = "root" 
