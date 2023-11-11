import cfg_id

cfg = cfg_id

P_info = cfg.P_info

TIMER_AD = 0x162A40

PLR_STRUCT_BASE_ADDRESS = 0x155130
PLR_STRUCT_SIZE = 0xAFC  # 3084

loop_address = PLR_STRUCT_BASE_ADDRESS
for n in P_info:
    n.dir_input.ad =    loop_address + 0x2EA
    n.button_input.ad = loop_address + 0x2ED
    n.macro_input.ad =  loop_address + 0x2EE

    loop_address += PLR_STRUCT_SIZE