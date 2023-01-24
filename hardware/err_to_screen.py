"""
Credit https://forums.openmv.io/t/how-can-i-get-the-line-number-of-error/6145
"""

import io
import sys

from hardware.esp32_oled_2_8_inch import display, drk_grn, sm_font
from hardware.esp32_oled_2_8_inch import draw_outline_box, clear_fill    
    
class errr(Exception):
    pass

def get_tb_text(e):
    buf = io.StringIO()
    sys.print_exception(e, buf)
    #Remove the word Traceback/etc
    return buf.getvalue()[34:]

def print_err(err):

    clear_fill()
    draw_outline_box()
    err_string=get_tb_text(err)
    
    scr_len  = 18
    max_rows = 12
    
    parts = [err_string[i : i + scr_len] for i in range(0, len(err_string), scr_len)]
    #parts.insert(0, f"{str(type(err))}: ") 
    
    count=0
    y_pos=5
    for x in parts:
        if count > max_rows:
            break
        else:
            display.draw_text(5, y_pos, x, sm_font, drk_grn)
        count+=1
        y_pos+=25  
        
    
