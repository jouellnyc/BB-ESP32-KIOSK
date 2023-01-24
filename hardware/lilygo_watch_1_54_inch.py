"""
http://www.lilygo.cn/prod_view.aspx?TypeId=50053&Id=1380&FId=t3:50053:3 
"""

from machine import Pin, SPI

import fonts.lily_go_watch_vga1_bold_16x32 as font
import axp202c
import st7789

from st7789 import color565
white=color565(255,255,255)
drk_grn=color565(50,100,30)
red=color565(255, 0, 0)
black=color565(0, 0, 0)


from bbapp.version import version

""" Variablize Pins here for Consistency                         """
""" These and below in tft_config don't have much room to change """

dc=27
cs=5
sck=18
mosi=19
backlight = 15

rotation  = 90

BFA = 80
TFA = 0


class Watch:
    
    """ Since the ili9341 screen were supported first, in order to support a """
    """ unified interface and the lilygo watch we need to make the watch     """
    """ function calls behave like the ili9341 driver                        """
    
    def __init__(self):
        #self.font    = font
        #self.red     = red
        #self.black   = black
        #self.drk_grn = drk_grn
        self.drk_grn = drk_grn
        self.white   = st7789.WHITE
        """ Only one font used on the tiny watch Screen ... """
        self.sm_font    = font
        self.score_font = font
        self.date_font  = font
        self.tft        = self.tft_config(rotation=rotation)
        self.tft.init()
        
    def tft_config(self, rotation=0, buffer_size=0, options=0):
        axp = axp202c.PMU()
        axp.enablePower(axp202c.AXP202_LDO2)
        return st7789.ST7789(
            SPI(1, baudrate=32000000, sck=Pin(sck, Pin.OUT), mosi=Pin(mosi, Pin.OUT)),
            240, 240, cs=Pin(cs, Pin.OUT),dc=Pin(dc, Pin.OUT),backlight=Pin(backlight, Pin.OUT),
            rotation=rotation, options=options, buffer_size=buffer_size)

    def draw_text(self, startx, starty, text, font, fg_text=st7789.WHITE, bg_text=st7789.BLACK):
        #Shorten Bottom
        if "Bottom" in text:
            text = text.replace("Bottom","Bot")
        
        words = text.split()
        #Shorten Year (YYYY) to (YY) 
        if "-" in words[0]:
            words[0] = words[0][:5]
            text = ' '.join(words)
        
        #Shorten to Final
        if "Final" in text:
            text = text.replace("Final Score","Final")
        
        #Shorten to time
        if "Game at" in text:
            words = text.split()
            if "-" in words[2]:
                words.pop(2)
                text = ' '.join(words)
        self.tft.text(font, text, startx, starty, fg_text, bg_text)

    def draw_outline_box(self):
        self.tft.hline(  0,   0, 239, self.white)
        self.tft.hline(  0, 237, 239, self.white)
        self.tft.hline(  0,  50, 239, self.white)
        self.tft.vline(  0,   0, 239, self.white)
        self.tft.vline(  239, 0, 239, self.white)

    def clear_fill(self):
        self.tft.fill(self.drk_grn)

    def print_setup(self, boot_stage):
        self.clear_fill()
        self.draw_outline_box()
        self.tft.text(self.sm_font, f"{boot_stage}"      , 5,   8, self.white, self.drk_grn)
        self.tft.text(self.sm_font, f"BB Kiosk"          , 5,  65, self.white, self.drk_grn)
        self.tft.text(self.sm_font, f"Version {version}" , 5, 105, self.white, self.drk_grn)
        
    def print_err(self, boot_stage):
        self.clear_fill()
        self.draw_outline_box()
        self.tft.text(self.sm_font, f"{boot_stage}"      , 5,   8, self.white, self.drk_grn)
        self.tft.text(self.sm_font, f"BB Kiosk"          , 5,  65, self.white, self.drk_grn)
        self.tft.text(self.sm_font, f"Version {version}" , 5, 105, self.white, self.drk_grn)

display = Watch()
