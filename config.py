import configparser
import os

keys_dict = {
    "HAT_CENTERED": 0,
    "HAT_DOWN": 4,
    "HAT_LEFT": 8,
    "HAT_LEFTDOWN": 12,
    "HAT_LEFTUP": 9,
    "HAT_RIGHT": 2,
    "HAT_RIGHTDOWN": 6,
    "HAT_RIGHTUP": 3,
    "HAT_UP": 1,

    "HWACCEL": 256,
    "HWPALETTE": 536870912,
    "HWSURFACE": 1,

    "IYUV_OVERLAY": 1448433993,

    "JOYAXISMOTION": 7,
    "JOYBALLMOTION": 8,
    "JOYBUTTONDOWN": 10,
    "JOYBUTTONUP": 11,
    "JOYHATMOTION": 9,

    "KEYDOWN": 2,
    "KEYUP": 3,

    "KMOD_ALT": 768,
    "KMOD_CAPS": 8192,
    "KMOD_CTRL": 192,
    "KMOD_LALT": 256,
    "KMOD_LCTRL": 64,
    "KMOD_LMETA": 1024,
    "KMOD_LSHIFT": 1,
    "KMOD_META": 3072,
    "KMOD_MODE": 16384,
    "KMOD_NONE": 0,
    "KMOD_NUM": 4096,
    "KMOD_RALT": 512,
    "KMOD_RCTRL": 128,
    "KMOD_RMETA": 2048,
    "KMOD_RSHIFT": 2,
    "KMOD_SHIFT": 3,

    "K_0": 48,
    "K_1": 49,
    "K_2": 50,
    "K_3": 51,
    "K_4": 52,
    "K_5": 53,
    "K_6": 54,
    "K_7": 55,
    "K_8": 56,
    "K_9": 57,
    "K_a": 97,
    "K_AMPERSAND": 38,
    "K_ASTERISK": 42,
    "K_AT": 64,
    "K_b": 98,
    "K_BACKQUOTE": 96,
    "K_BACKSLASH": 92,
    "K_BACKSPACE": 8,
    "K_BREAK": 318,
    "K_c": 99,
    "K_CAPSLOCK": 301,
    "K_CARET": 94,
    "K_CLEAR": 12,
    "K_COLON": 58,
    "K_COMMA": 44,
    "K_d": 100,
    "K_DELETE": 127,
    "K_DOLLAR": 36,
    "K_DOWN": 274,
    "K_e": 101,
    "K_END": 279,
    "K_EQUALS": 61,
    "K_ESCAPE": 27,
    "K_EURO": 321,
    "K_EXCLAIM": 33,
    "K_f": 102,
    "K_F1": 282,
    "K_F10": 291,
    "K_F11": 292,
    "K_F12": 293,
    "K_F13": 294,
    "K_F14": 295,
    "K_F15": 296,
    "K_F2": 283,
    "K_F3": 284,
    "K_F4": 285,
    "K_F5": 286,
    "K_F6": 287,
    "K_F7": 288,
    "K_F8": 289,
    "K_F9": 290,
    "K_FIRST": 0,
    "K_g": 103,
    "K_GREATER": 62,
    "K_h": 104,
    "K_HASH": 35,
    "K_HELP": 315,
    "K_HOME": 278,
    "K_i": 105,
    "K_INSERT": 277,
    "K_j": 106,
    "K_k": 107,
    "K_KP0": 256,
    "K_KP1": 257,
    "K_KP2": 258,
    "K_KP3": 259,
    "K_KP4": 260,
    "K_KP5": 261,
    "K_KP6": 262,
    "K_KP7": 263,
    "K_KP8": 264,
    "K_KP9": 265,

    "K_KP_DIVIDE": 267,
    "K_KP_ENTER": 271,
    "K_KP_EQUALS": 272,
    "K_KP_MINUS": 269,
    "K_KP_MULTIPLY": 268,
    "K_KP_PERIOD": 266,
    "K_KP_PLUS": 270,

    "K_l": 108,
    "K_LALT": 308,
    "K_LAST": 323,
    "K_LCTRL": 306,
    "K_LEFT": 276,
    "K_LEFTBRACKET": 91,
    "K_LEFTPAREN": 40,
    "K_LESS": 60,
    "K_LMETA": 310,
    "K_LSHIFT": 304,
    "K_LSUPER": 311,
    "K_m": 109,
    "K_MENU": 319,
    "K_MINUS": 45,
    "K_MODE": 313,
    "K_n": 110,
    "K_NUMLOCK": 300,
    "K_o": 111,
    "K_p": 112,
    "K_PAGEDOWN": 281,
    "K_PAGEUP": 280,
    "K_PAUSE": 19,
    "K_PERIOD": 46,
    "K_PLUS": 43,
    "K_POWER": 320,
    "K_PRINT": 316,
    "K_q": 113,
    "K_QUESTION": 63,
    "K_QUOTE": 39,
    "K_QUOTEDBL": 34,
    "K_r": 114,
    "K_RALT": 307,
    "K_RCTRL": 305,
    "K_RETURN": 13,
    "K_RIGHT": 275,
    "K_RIGHTBRACKET": 93,
    "K_RIGHTPAREN": 41,
    "K_RMETA": 309,
    "K_RSHIFT": 303,
    "K_RSUPER": 312,
    "K_s": 115,
    "K_SCROLLOCK": 302,
    "K_SEMICOLON": 59,
    "K_SLASH": 47,
    "K_SPACE": 32,
    "K_SYSREQ": 317,
    "K_t": 116,
    "K_TAB": 9,
    "K_u": 117,
    "K_UNDERSCORE": 95,
    "K_UNKNOWN": 0,
    "K_UP": 273,
    "K_v": 118,
    "K_w": 119,
    "K_x": 120,
    "K_y": 121,
    "K_z": 122

}


def create_config(path):
    # Create default config file in .ini format
    config = configparser.ConfigParser()

    config.add_section('PlayerMovementControls')
    config.set('PlayerMovementControls', 'forward', 'K_w')
    config.set('PlayerMovementControls', 'backward', 'K_s')
    config.set('PlayerMovementControls', 'left', 'K_a')
    config.set('PlayerMovementControls', 'right', 'K_d')

    with open(path, "w") as config_file:
        config.write(config_file)


# ----------------------------------------------------------------


def get_config(path):
    # Create config obj
    if not os.path.exists('config.ini'):
        create_config(path)
    config = configparser.ConfigParser()
    config.read(path)
    return config


CONFIG = get_config('config.ini')
