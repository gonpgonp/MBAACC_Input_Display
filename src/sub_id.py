from ctypes import windll, wintypes, byref
from struct import unpack, pack
import os
import time
import copy
import ctypes
import psutil
import math

import cfg_id
import ad_id
cfg = cfg_id
ad = ad_id

wintypes = ctypes.wintypes
windll = ctypes.windll
create_string_buffer = ctypes.create_string_buffer
byref = ctypes.byref
WriteMem = windll.kernel32.WriteProcessMemory
ReadMem = windll.kernel32.ReadProcessMemory
OpenProcess = windll.kernel32.OpenProcess
Module32Next = windll.kernel32.Module32Next
Module32First = windll.kernel32.Module32First
CreateToolhelp32Snapshot = windll.kernel32.CreateToolhelp32Snapshot
CloseHandle = windll.kernel32.CloseHandle
sizeof = ctypes.sizeof

class MODULEENTRY32(ctypes.Structure):
    _fields_ = [
        ("dwSize",             wintypes.DWORD),
        ("th32ModuleID",       wintypes.DWORD),
        ("th32ProcessID",      wintypes.DWORD),
        ("GlblcntUsage",       wintypes.DWORD),
        ("ProccntUsage",       wintypes.DWORD),
        ("modBaseAddr",        ctypes.POINTER(wintypes.BYTE)),
        ("modBaseSize",        wintypes.DWORD),
        ("hModule",            wintypes.HMODULE),
        ("szModule",           ctypes.c_byte * 256),
        ("szExePath",          ctypes.c_byte * 260),
    ]


def pidget():
    dict_pids = {
        p.info["name"]: p.info["pid"]
        for p in psutil.process_iter(attrs=["name", "pid"])
    }
    return dict_pids


def get_base_addres():
    cfg.pid = 0
    while cfg.pid == 0:
        dict_pids = pidget()
        try:
            cfg.pid = dict_pids["MBAA.exe"]
        except:
            os.system('cls')
            print("Waiting for MBAA to start")
            time.sleep(0.2)

    cfg.h_pro = OpenProcess(0x1F0FFF, False, cfg.pid)

    # MODULEENTRY32を取得
    snapshot = CreateToolhelp32Snapshot(0x00000008, cfg.pid)

    lpme = MODULEENTRY32()
    lpme.dwSize = sizeof(lpme)

    res = Module32First(snapshot, byref(lpme))

    while cfg.pid != lpme.th32ProcessID:
        res = Module32Next(snapshot, byref(lpme))

    b_baseAddr = create_string_buffer(8)
    b_baseAddr.raw = lpme.modBaseAddr

    cfg.base_ad = unpack('q', b_baseAddr.raw)[0]


def b_unpack(d_obj):
    num = 0
    num = len(d_obj)
    if num == 1:
        return unpack('b', d_obj.raw)[0]
    elif num == 2:
        return unpack('h', d_obj.raw)[0]
    elif num == 4:
        return unpack('l', d_obj.raw)[0]

def r_mem(ad, b_obj):
    ReadMem(cfg.h_pro, ad + cfg.base_ad, b_obj, len(b_obj), None)
    return b_unpack(b_obj)


def para_get(obj):
    obj.num = r_mem(obj.ad, obj.b_dat)


def ex_cmd_enable():
    INVALID_HANDLE_VALUE = -1
    STD_INPUT_HANDLE = -10
    STD_OUTPUT_HANDLE = -11
    STD_ERROR_HANDLE = -12
    ENABLE_VIRTUAL_TERMINAL_PROCESSING = 0x0004
    ENABLE_LVB_GRID_WORLDWIDE = 0x0010

    hOut = windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
    if hOut == INVALID_HANDLE_VALUE:
        return False
    dwMode = wintypes.DWORD()
    if windll.kernel32.GetConsoleMode(hOut, byref(dwMode)) == 0:
        return False
    dwMode.value |= ENABLE_VIRTUAL_TERMINAL_PROCESSING
    # dwMode.value |= ENABLE_LVB_GRID_WORLDWIDE
    if windll.kernel32.SetConsoleMode(hOut, dwMode) == 0:
        return False
    return True


def situationCheck():
    for n in cfg.P_info:
        n.prev_dir_input = n.dir_input.num
        n.prev_button_input = n.button_input.num
        n.prev_macro_input = n.macro_input.num
        para_get(n.dir_input)
        para_get(n.button_input)
        para_get(n.macro_input)
    

def view_st():
    # キャラの状況推移表示
    for n in cfg.P_info:
        if (n.prev_dir_input    != n.dir_input.num or
            n.prev_button_input != n.button_input.num or
            n.prev_macro_input  != n.macro_input.num):
            
            input_add(n)
        n.timer_array[0] += 1
        
def text_font(rgb):
    Text_font_str = "\x1b[38;2;" + str(rgb[0]) + ";" + str(rgb[1]) + ";" + str(rgb[2]) + "m"
    return Text_font_str


def bg_font(rgb):
    bg_font_str = "\x1b[48;2;" + str(rgb[0]) + ";" + str(rgb[1]) + ";" + str(rgb[2]) + "m"
    return bg_font_str


def get_font(text_rgb, bg_rgb):
    return text_font(text_rgb) + bg_font(bg_rgb)


def clear_arrays():
    for n in cfg.P_info:
        n.timer_array = [0] * cfg.num_rows
        n.button_array = ["     "] * cfg.num_rows
        n.dir_array = [" "] * cfg.num_rows


def input_add(n):
    DEF = '\x1b[0m'

    a_font = get_font((255, 143, 169), (170, 27, 58))
    b_font = get_font((255, 255, 137), (169, 91, 7))
    c_font = get_font((143, 255, 195), (18, 132, 62))
    d_font = get_font((137, 255, 255), (21, 66, 161))
    e_font = get_font((255, 140, 255), (164, 39, 189))
    
    n.button_array = ["     "] + n.button_array[:-1]
    n.dir_array = [" "] + n.dir_array[:-1]
    n.timer_array = [0] + n.timer_array[:-1]
    
    buttons = ""
    if n.button_input.num & 16 > 0:
        buttons += a_font + "A" + "*"
    else:
        buttons += " "
    
    if n.button_input.num & 32 > 0:
        buttons += b_font + "B" + "*"
    else:
        buttons += " "
    
    if n.button_input.num & 64 > 0:
        buttons += c_font + "C" + "*"
    else:
        buttons += " "
    
    if n.button_input.num & 128 > 0:
        buttons += d_font + "D" + "*"
    else:
        buttons += " "
    
    if n.macro_input.num != 0:
        buttons += e_font + "E" + "*"
    else:
        buttons += " "
    
    n.button_array[0] = buttons
    
    direction = " "
    if n.dir_input.num == 0:
        directon = " "
    else:
        direction = str(n.dir_input.num)
    
    n.dir_array[0] = direction

def view():
    END = '\x1b[0m' + '\x1b[49m' + '\x1b[K' + '\x1b[1E'
    print_str = "\x1b[1;1H" + "\x1b[?25l"
    print_str += "\x1b[4m P1           | P2          \x1b[0m" + END
    
    DEF = '\x1b[0m'
    alt_row = DEF + "\x1b[48;5;234m"
    
    for i in range(cfg.num_rows):
        d1 = cfg.P1.dir_array[i]
        b1 = cfg.P1.button_array[i]
        t1 = str(cfg.P1.timer_array[i]).rjust(3, ' ')[-3:]
        
        d2 = cfg.P2.dir_array[i]
        b2 = cfg.P2.button_array[i]
        t2 = str(cfg.P2.timer_array[i]).rjust(3, ' ')[-3:]
        
        if i % 2 == 1:
            b1 = b1.replace("*", alt_row)
            b2 = b2.replace("*", alt_row)
            print_str += (  f" {alt_row}{d1} {b1}  {t1} |" +
                            f" {alt_row}{t2}  {b2} {d2}" + END)
        else:
            b1 = b1.replace("*", DEF)
            b2 = b2.replace("*", DEF)
            print_str += (  f" {d1} {b1}  {t1} |" +
                            f" {t2}  {b2} {d2}" + END)
    
    print(print_str)
    

def timer_check():
    cfg.f_timer = r_mem(ad.TIMER_AD, cfg.b_timer)
