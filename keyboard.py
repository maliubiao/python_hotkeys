#-*-encoding=utf-8-*-
import struct

def parse_struct(b, fmt): 
    d = {}
    fmts = "".join([x[1] for x in fmt])
    raw = b.read(struct.calcsize(fmts)) 
    raw = struct.unpack(fmts, raw)   
    for i, item in enumerate(fmt):
        d[item[0]]= raw[i]
    return d 

def parse_event(b):
    return parse_struct(b, input_event)

def new_struct(d, fmt): 
    l = []
    fmts = "".join([x[1] for x in fmt]) 
    for i in fmt:    
        l.append(d[i[0]])
    return struct.pack(fmts, *l)


input_event = (
        ("tv_sec", "I"),
        ("tv_usec", "Q"),
        ("type", "H"),
        ("code", "H"),
        ("value", "i")
        ) 

PRESSED = 1
RELEASED = 0
REPEATED = 2

#Used as markers to separate events 
EV_SYN = 0x00
#used to describe state changes of keyboards, buttons, or other key-like devices 
EV_KEY = 0x01
#used to describe relative axis value changes 
EV_REL = 0x02
#used to describe absoute axis value changes
EV_ABS = 0x03 
#used to describe miscellaneous input data that do not fit into other types
EV_MSC = 0x04
#used to describe binary state input switches
EV_SW  = 0x05
#used to turn leds on devices on and off
EV_LED = 0x11
#used to ouput sound to devices
EV_SND = 0x12
#used for autorepeating devices
EV_REP = 0x14
#used to send force feedback commands to and input device
EV_FF  = 0x15
#a special type for power button and switch input
EV_PWR = 0x16
#used to receive force feedback device status
EV_FF_STATUS = 0x17
EV_MAX = 0x1f

ev_table = {
    0: 'EV_SYN',
    1: 'EV_KEY',
    2: 'EV_REL',
    3: 'EV_ABS',
    4: 'EV_MSC',
    5: 'EV_SW',
    17: 'EV_LED',
    18: 'EV_SND',
    20: 'EV_REP',
    21: 'EV_FF',
    22: 'EV_PWR',
    23: 'EV_FF_STATUS',
    31: 'EV_MAX'
    } 


RESERVED = 0
ESC =  1
NUM_1 =  2
NUM_2 =  3
NUM_3 =  4
NUM_4 =  5
NUM_5 =  6
NUM_6 =  7
NUM_7 =  8
NUM_8 =  9
NUM_9 =  10
NUM_0 =  11
MINUS = 12
EQUAL = 13
BACKSPACE = 14
TAB =  15
Q =  16
W =  17
E =  18
R =  19
T =  20
Y =  21
U =  22
I =  23
O =  24
P =  25
LEFTBRACE = 26
RIGHTBRACE = 27
ENTER = 28
LEFTCTRL = 29
A =  30
S =  31
D =  32
F =  33
G =  34
H =  35
J =  36
K =  37
L =  38
SEMICOLON = 39
APOSTROPHE = 40
GRAVE = 41
LEFTSHIFT = 42
BACKSLASH = 43
Z =  44
X =  45
C =  46
V =  47
B =  48
N =  49
M =  50
COMMA = 51
DOT =  52
SLASH = 53
RIGHTSHIFT = 54
KPASTERISK = 55
LEFTALT = 56
SPACE = 57
CAPSLOCK = 58
F1 =  59
F2 =  60
F3 =  61
F4 =  62
F5 =  63
F6 =  64
F7 =  65
F8 =  66
F9 =  67
F10 =  68
NUMLOCK = 69
SCROLLLOCK = 70
KP7 =  71
KP8 =  72
KP9 =  73
KPMINUS = 74
KP4 =  75
KP5 =  76
KP6 =  77
KPPLUS = 78
KP1 =  79
KP2 =  80
KP3 =  81
KP0 =  82
KPDOT = 83

ZENKAKUHANKAKU = 85
ND102 = 86
F11 =  87
F12 =  88
RO =  89
KATAKANA = 90
HIRAGANA = 91
HENKAN = 92
KATAKANAHIRAGANA =  93
MUHENKAN = 94
KPJPCOMMA = 95
KPENTER = 96
RIGHTCTRL = 97
KPSLASH = 98
SYSRQ = 99
RIGHTALT = 100
LINEFEED = 101
HOME = 102
UP =  103
PAGEUP = 104
LEFT = 105
RIGHT = 106
END =  107
DOWN = 108
PAGEDOWN = 109
INSERT = 110
DELETE = 111
MACRO = 112
MUTE = 113
VOLUMEDOWN = 114
VOLUMEUP = 115
#SC System Power Down
POWER = 116 
KPEQUAL = 117
KPPLUSMINUS = 118
PAUSE = 119
#AL Compiz Scale (Expose)
SCALE = 120

KPCOMMA = 121
HANGEUL = 122
HANGUEL = HANGEUL
HANJA = 123
YEN =  124
LEFTMETA = 125
RIGHTMETA = 126
COMPOSE = 127

#AC Stop
STOP = 128
AGAIN = 129
#AC Properties
PROPS = 130 
#AC Undo
UNDO = 131
FRONT = 132
#AC Copy 
COPY = 133
#AC Open
OPEN = 134
#AC Paste
PASTE = 135
#AC Search 
FIND = 136
#AC Cut 
CUT =  137
#AL Integrated Help Center
HELP = 138
#(show menu)
MENU = 139
#AL Calculator
CALC = 140
SETUP = 141
#SC System Sleep 
SLEEP = 142
#System Wake Up
WAKEUP = 143
#AL Local Machine Browser
FILE = 144
SENDFILE = 145
DELETEFILE = 146
XFER = 147
PROG1 = 148
PROG2 = 149
#AL Internet Browser
WWW =  150
MSDOS = 151
#AL Terminal Lock/Screensaver
COFFEE = 152
SCREENLOCK = COFFEE
DIRECTION = 153
CYCLEWINDOWS = 154
MAIL = 155
#AC Bookmarks
BOOKMARKS = 156
COMPUTER = 157
#AC Back 
BACK = 158
#AC Forward 
FORWARD = 159
CLOSECD = 160
EJECTCD = 161
EJECTCLOSECD = 162
NEXTSONG = 163
PLAYPAUSE = 164
PREVIOUSSONG = 165
STOPCD = 166
RECORD = 167
REWIND = 168
#Media Select Telephone
PHONE = 169
ISO =  170
#AL Consumer Control Configuration
CONFIG = 171
#AC Home 
HOMEPAGE = 172
#AC Refresh
REFRESH = 173
#AC Exit
EXIT = 174
MOVE = 175
EDIT = 176
SCROLLUP = 177
SCROLLDOWN = 178
KPLEFTPAREN = 179
KPRIGHTPAREN  = 180
#AC New 
NEW =  181 
#AC Redo/Repeat
REDO = 182 

F13 =  183
F14 =  184
F15 =  185
F16 =  186
F17 =  187
F18 =  188
F19 =  189
F20 =  190
F21 =  191
F22 =  192
F23 =  193
F24 =  194

PLAYCD = 200
PAUSECD = 201
PROG3 = 202
PROG4 = 203
#AL Dashboard
DASHBOARD = 204
SUSPEND = 205
#AC Close
CLOSE = 206
PLAY = 207
FASTFORWARD = 208
BASSBOOST = 209
#AC Print
PRINT = 210
HP =  211
CAMERA = 212
SOUND = 213
QUESTION = 214
EMAIL = 215
CHAT = 216
SEARCH = 217
CONNECT = 218
FINANCE = 219
SPORT = 220
SHOP = 221
ALTERASE = 222
#AC Cancel
CANCEL = 223
BRIGHTNESSDOWN = 224
BRIGHTNESSUP  = 225
MEDIA = 226

#Cycle between available video
SWITCHVIDEOMODE = 227

KBDILLUMTOGGLE  = 228
KBDILLUMDOWN  = 229
KBDILLUMUP = 230

#AC Send
SEND = 231
#AC Reply
REPLY = 232
#AC Forward Msg
FORWARDMAIL = 233
#AC Save
SAVE = 234
DOCUMENTS = 235

BATTERY = 236

BLUETOOTH = 237
WLAN = 238
UWB =  239

UNKNOWN = 240

#drive next video source
VIDEO_NEXT = 241
#drive previous video source
VIDEO_PREV = 242
#brightness up, after max is min
BRIGHTNESS_CYCLE  = 243
#Set Auto Brightness: manual 
BRIGHTNESS_AUTO  = 244
BRIGHTNESS_ZERO  = BRIGHTNESS_AUTO
#display device to off state
DISPLAY_OFF = 245

#Wireless WAN (LTE, UMTS, GSM, etc.)
WWAN = 246
WIMAX = WWAN
#Key that controls all radios
RFKILL = 247

#Mute / unmute the microphone
MICMUTE = 248

key_table = {
     0: 'RESERVED',
     1: 'ESC',
     2: '1',
     3: '2',
     4: '3',
     5: '4',
     6: '5',
     7: '6',
     8: '7',
     9: '8',
     10: '9',
     11: '0',
     12: 'MINUS',
     13: 'EQUAL',
     14: 'BACKSPACE',
     15: 'TAB',
     16: 'Q',
     17: 'W',
     18: 'E',
     19: 'R',
     20: 'T',
     21: 'Y',
     22: 'U',
     23: 'I',
     24: 'O',
     25: 'P',
     26: 'LEFTBRACE',
     27: 'RIGHTBRACE',
     28: 'ENTER',
     29: 'LEFTCTRL',
     30: 'A',
     31: 'S',
     32: 'D',
     33: 'F',
     34: 'G',
     35: 'H',
     36: 'J',
     37: 'K',
     38: 'L',
     39: 'SEMICOLON',
     40: 'APOSTROPHE',
     41: 'GRAVE',
     42: 'LEFTSHIFT',
     43: 'BACKSLASH',
     44: 'Z',
     45: 'X',
     46: 'C',
     47: 'V',
     48: 'B',
     49: 'N',
     50: 'M',
     51: 'COMMA',
     52: 'DOT',
     53: 'SLASH',
     54: 'RIGHTSHIFT',
     55: 'KPASTERISK',
     56: 'LEFTALT',
     57: 'SPACE',
     58: 'CAPSLOCK',
     59: 'F1',
     60: 'F2',
     61: 'F3',
     62: 'F4',
     63: 'F5',
     64: 'F6',
     65: 'F7',
     66: 'F8',
     67: 'F9',
     68: 'F10',
     69: 'NUMLOCK',
     70: 'SCROLLLOCK',
     71: 'KP7',
     72: 'KP8',
     73: 'KP9',
     74: 'KPMINUS',
     75: 'KP4',
     76: 'KP5',
     77: 'KP6',
     78: 'KPPLUS',
     79: 'KP1',
     80: 'KP2',
     81: 'KP3',
     82: 'KP0',
     83: 'KPDOT',
     85: 'ZENKAKUHANKAKU',
     86: '102ND',
     87: 'F11',
     88: 'F12',
     89: 'RO',
     90: 'KATAKANA',
     91: 'HIRAGANA',
     92: 'HENKAN',
     93: 'KATAKANAHIRAGANA',
     94: 'MUHENKAN',
     95: 'KPJPCOMMA',
     96: 'KPENTER',
     97: 'RIGHTCTRL',
     98: 'KPSLASH',
     99: 'SYSRQ',
     100: 'RIGHTALT',
     101: 'LINEFEED',
     102: 'HOME',
     103: 'UP',
     104: 'PAGEUP',
     105: 'LEFT',
     106: 'RIGHT',
     107: 'END',
     108: 'DOWN',
     109: 'PAGEDOWN',
     110: 'INSERT',
     111: 'DELETE',
     112: 'MACRO',
     113: 'MUTE',
     114: 'VOLUMEDOWN',
     115: 'VOLUMEUP',
     116: 'POWER',
     117: 'KPEQUAL',
     118: 'KPPLUSMINUS',
     119: 'PAUSE',
     120: 'SCALE',
     121: 'KPCOMMA',
     122: 'HANGUEL',
     123: 'HANJA',
     124: 'YEN',
     125: 'LEFTMETA',
     126: 'RIGHTMETA',
     127: 'COMPOSE',
     128: 'STOP',
     129: 'AGAIN',
     130: 'PROPS',
     131: 'UNDO',
     132: 'FRONT',
     133: 'COPY',
     134: 'OPEN',
     135: 'PASTE',
     136: 'FIND',
     137: 'CUT',
     138: 'HELP',
     139: 'MENU',
     140: 'CALC',
     141: 'SETUP',
     142: 'SLEEP',
     143: 'WAKEUP',
     144: 'FILE',
     145: 'SENDFILE',
     146: 'DELETEFILE',
     147: 'XFER',
     148: 'PROG1',
     149: 'PROG2',
     150: 'WWW',
     151: 'MSDOS',
     152: 'COFFEE',
     153: 'DIRECTION',
     154: 'CYCLEWINDOWS',
     155: 'MAIL',
     156: 'BOOKMARKS',
     157: 'COMPUTER',
     158: 'BACK',
     159: 'FORWARD',
     160: 'CLOSECD',
     161: 'EJECTCD',
     162: 'EJECTCLOSECD',
     163: 'NEXTSONG',
     164: 'PLAYPAUSE',
     165: 'PREVIOUSSONG',
     166: 'STOPCD',
     167: 'RECORD',
     168: 'REWIND',
     169: 'PHONE',
     170: 'ISO',
     171: 'CONFIG',
     172: 'HOMEPAGE',
     173: 'REFRESH',
     174: 'EXIT',
     175: 'MOVE',
     176: 'EDIT',
     177: 'SCROLLUP',
     178: 'SCROLLDOWN',
     179: 'KPLEFTPAREN',
     180: 'KPRIGHTPAREN',
     181: 'NEW',
     182: 'REDO',
     183: 'F13',
     184: 'F14',
     185: 'F15',
     186: 'F16',
     187: 'F17',
     188: 'F18',
     189: 'F19',
     190: 'F20',
     191: 'F21',
     192: 'F22',
     193: 'F23',
     194: 'F24',
     200: 'PLAYCD',
     201: 'PAUSECD',
     202: 'PROG3',
     203: 'PROG4',
     204: 'DASHBOARD',
     205: 'SUSPEND',
     206: 'CLOSE',
     207: 'PLAY',
     208: 'FASTFORWARD',
     209: 'BASSBOOST',
     210: 'PRINT',
     211: 'HP',
     212: 'CAMERA',
     213: 'SOUND',
     214: 'QUESTION',
     215: 'EMAIL',
     216: 'CHAT',
     217: 'SEARCH',
     218: 'CONNECT',
     219: 'FINANCE',
     220: 'SPORT',
     221: 'SHOP',
     222: 'ALTERASE',
     223: 'CANCEL',
     224: 'BRIGHTNESSDOWN',
     225: 'BRIGHTNESSUP',
     226: 'MEDIA',
     227: 'SWITCHVIDEOMODE',
     228: 'KBDILLUMTOGGLE',
     229: 'KBDILLUMDOWN',
     230: 'KBDILLUMUP',
     231: 'SEND',
     232: 'REPLY',
     233: 'FORWARDMAIL',
     234: 'SAVE',
     235: 'DOCUMENTS',
     236: 'BATTERY',
     237: 'BLUETOOTH',
     238: 'WLAN',
     239: 'UWB',
     240: 'UNKNOWN',
     241: 'VIDEO_NEXT',
     242: 'VIDEO_PREV',
     243: 'BRIGHTNESS_CYCLE',
     244: 'BRIGHTNESS_AUTO',
     245: 'DISPLAY_OFF',
     246: 'WIMAX',
     247: 'RFKILL',
     248: 'MICMUTE'
     } 

