from ctypes import windll
from struct import unpack
import os
import time
import cfg_id
import ad_id

import sub_id
ad = ad_id
cfg = cfg_id
sub = sub_id

sub.ex_cmd_enable()
os.system(f'mode con: cols=32 lines={cfg.num_rows + 3}')
os.system('cls')
os.system('title MBAACC Input Display')
print('\x1b[1;1H' + '\x1b[?25l')
windll.winmm.timeBeginPeriod(1)  # タイマー精度を1msec単位にする

# 変数初期化
start_time = time.time()

# ベースアドレス取得
sub.get_base_addres()

while 1:
    time.sleep(0.002)

    # タイマーチェック
    sub.timer_check()

    # フレームの切り替わりを監視
    if (cfg.f_timer != cfg.f_timer2):

        cfg.f_timer2 = cfg.f_timer
        time.sleep(0.001)

        # 各種数値の取得
        sub.situationCheck()

        # ゲーム状況の取得
        sub.view_st()

        if cfg.f_timer == 1:
            sub.clear_arrays()
    sub.view()
