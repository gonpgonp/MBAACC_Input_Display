from ctypes import create_string_buffer
num_rows = 32

class para:
    def __init__(self, byte_len):
        self.ad = 0x00
        self.num = 0
        self.b_dat = create_string_buffer(byte_len)

class Character_info:
    def __init__(self):
        self.dir_input = para(1)
        self.button_input = para(1)
        self.macro_input = para(1)
        self.prev_dir_input = 0
        self.prev_button_input = 0
        self.prev_macro_input = 0
        self.button_array = ["     "] * num_rows
        self.dir_array = [" "] * num_rows
        self.timer = 0
        self.timer_array = [0] * num_rows

P_info = [Character_info(), Character_info()]

pid = 0
h_pro = 0
base_ad = 0
f_timer = 0
b_timer = create_string_buffer(4)
f_timer2 = 0

P1 = P_info[0]
P2 = P_info[1]
