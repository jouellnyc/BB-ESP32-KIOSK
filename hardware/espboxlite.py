""" These value are for the ESP32-S3-BOX-LITE """
from machine import Pin, SPI, ADC

from .ili9341 import color565, Display

from .font_runner import sm_font, score_font, date_font
from bbapp.version import version

""" BOX-LITE specifics """
#NOTE: S3-ESP32-BOX-LITE - INVERTED w/ili9341
drk_grn=color565(255,222,255)
white=color565(0, 0, 0)
black=color565(255,255,255)
red=color565(255, 0, 0)

dc=4
cs=5
rst=48
width=320
height=240
rotation=180

spi = SPI(1, baudrate=40000000, sck=Pin(7), mosi=Pin(6))
display = Display(spi, dc=Pin(dc), cs=Pin(cs), rst=Pin(rst), width=width, height=height, rotation=rotation)

adc = ADC(Pin(1))
""" We only check  Button 3 - It's on GPIO01
#Unpushed
>>> adc.read_u16()
65535

#Pushed
>>> adc.read_u16()
55261
"""


def draw_outline_box():
    display.draw_vline(0,    0, 240, white)
    display.draw_vline(319,  0, 240, white)
    display.draw_hline(0,    0, 320, white)
    display.draw_hline(0,   40, 320, white)
    display.draw_hline(0,  239, 320, white)
    
def clear_fill():
    display.clear()
    display.fill_rectangle(0,0, 320, 240, drk_grn)            
        
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
    
def scroll_print(text='NA',x_pos=5, y_pos=5, scr_len=30, Error=False, clear=True, font=sm_font, bg=drk_grn, fg=white):

    """ Pass in a 'text container'                  """
    """ Either and instance of an error or a string """
    if clear:
        display.clear_fill()
        display.draw_outline_box()
    
    """ If an error instance, pull out the text """
    if Error:
        text=get_tb_text(text)
        
    max_rows = 12
    parts = [text[i : i + scr_len] for i in range(0, len(text), scr_len)]
    
    count=0
    for text in parts:
        if count > max_rows:
            break
        else:
            display.draw_text(x_pos, y_pos, text, font=font, color=fg,  background=bg)
            print(text)
        count+=1
        #y_pos+=25  sm font
        y_pos+=28   #date font

def check_button3():
    if str(adc.read_u16()).startswith('55'):
        return True

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
display.get_tb_text      = get_tb_text
display.scroll_print     = scroll_print
display.check_button3    = check_button3
