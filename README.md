##Linux下无视桌面环境的全局快捷键方案
###配置文件为hotkey_config.py 
```python 
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
USER = "richard" 
```

###权限
需要root以读取键盘事件, 在hotkey_config.py里修改USER，这样在执行必要的操作后会以USER执行相应的命令, 如果不修改则命令以root方式执行，很危险.

###执行
先根据示例修改配置, 然后以root执行
```shell
python hotkey.py
```

###响应规则
1. 如果同时存在CTRL + M,  CRTL, 则只响应CRTL
2. 如果存在重复定义, 则只响应第一个
3. 按下快捷键不放只响应一次 
4. 对桌面环境无干扰

###系统环境
只能在Linux上执行, 桌面环境不重要(没有也可以)， 需要python支持select.epoll
如果在桌面环境下使用，需要确定~/.Xauthority是否存在，不存在会无法执行图形界面的程序 
由于硬件相关, 程序会自动检测键盘(默认是监听所有键盘), 检测不到是有可能的.


###可用的键码 
参考keyboard.py, 太长, 这里就不写了.

欢迎fork, 欢迎反馈

