""" All ili9341's seem to have the same SCK/MOSI settings """
""" But dc, cs, rst seem to vary                          """

from machine import Pin, SPI
spi = SPI(2, baudrate=51200000, sck=Pin(18), mosi=Pin(23))

from .ili9341 import color565, Display
white=color565(255,255,255)
drk_grn=color565(50,100,30)
red=color565(255, 0, 0)
black=color565(0, 0, 0)

from bbapp.version import version
from .font_runner import sm_font, score_font, date_font
from .config import case, wires, screen

if screen == 'lilygo_ili9341_2_4':
    
    from .lily_go_2_4_inch import dc, cs, rst
    
elif screen == 'esp32_ili9341_2_8':
    
    from .esp32_2_8_inch import dc, cs, rst

if case == "sideways":

        v13 = 239 ; v21 = 319 ; h13 = 319 ; h23 = 319 ; h32 = 239 ; h33 = 319
        
        """ Sideways case: https://github.com/jouellnyc/BB-ESP32-KIOSK/blob/main/images/orange.png """
        #This is for when the wires are on the right of the sideways case
        
        if wires == "right":

            width=320; height=240; rotation=270
            
        elif wires == "left":
            
            #This is for when the wires are on the left of the sideways case
            width=320; height=240; rotation=90

elif case == "upright":
        
        v13 = 319 ; v21 = 239 ; h13 = 239 ; h23 = 239 ; h32 = 319 ; h33 = 239
        """ Use the small font if upright so it fits """
        date_font=sm_font
    
        """ Upright case: https://github.com/jouellnyc/BB-ESP32-KIOSK/blob/main/images/side_view_black.jpg """
        if wires == "top":
            #This is for when the wires are on the top  of the upright case
            width=240; height=320; rotation=0
            
        elif wires == "bottom":
            #This is for when the wires are on the top  of the upright case
            width=240; height=320; rotation=180
            #box lite
            #width=320; height=240; rotation=180
            
display = Display(spi, dc=Pin(dc), cs=Pin(cs), rst=Pin(rst), width=width, height=height, rotation=rotation)

def draw_outline_box():
    display.draw_vline(0,   0, v13, white)
    display.draw_vline(v21, 0, 239, white)
    display.draw_hline(h13, 0, 319, white)
    display.draw_hline(0,  40, h23, white)
    display.draw_hline(0, h33, h32, white)
    
def draw_outline_box():
    display.draw_vline(0,    0, 240, white)
    display.draw_vline(319,  0, 240, white)
    display.draw_hline(0,  239, 320, white)
    display.draw_hline(0,    0, 320, white)
    display.draw_hline(0,   40, 320, white)

    
def clear_fill():
    display.clear()
    display.fill_rectangle(0,0, h23, h32, drk_grn)        
        
def print_setup(boot_stage):
    clear_fill()    
    draw_outline_box()
    display.draw_text(5, 8,  f"{boot_stage}"       , date_font, white, drk_grn)
    display.draw_text(5, 65, 'BB Kiosk'            , date_font, white, drk_grn)
    display.draw_text(5, 105, f"Version {version}" , date_font, white, drk_grn)

def get_tb_text(err):
    """
    Credit https://forums.openmv.io/t/how-can-i-get-the-line-number-of-error/6145
    """
    import io
    import sys
    buf = io.StringIO()
    sys.print_exception(err, buf)
    #Remove the word Traceback/etc
    return buf.getvalue()[35:]
    
def print_err(err):

    display.clear_fill()
    display.draw_outline_box()
    
    err_string=get_tb_text(err)
    scr_len  = 30
    max_rows = 12
    
    parts = [err_string[i : i + scr_len] for i in range(0, len(err_string), scr_len)]
    
    count=0
    y_pos=5
    
    for x in parts:
        if count > max_rows:
            break
        else:
            display.draw_text(5, y_pos, x, sm_font, drk_grn)
            print(x)
        count+=1
        y_pos+=25  

display.draw_outline_box = draw_outline_box
display.clear_fill       = clear_fill
display.print_setup      = print_setup
display.white            = white
display.drk_grn          = drk_grn
display.red              = red
display.black            = black
display.sm_font          = sm_font
display.score_font       = score_font
display.date_font        = date_font
display.print_err        = print_err