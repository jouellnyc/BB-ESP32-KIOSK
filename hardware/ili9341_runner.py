""" All ili9341's seem to have the same SCK/MOSI settings """
""" But dc, cs, rst seem to vary                          """

from machine import Pin, SPI
spi = SPI(2, baudrate=51200000, sck=Pin(18), mosi=Pin(23))

from .ili9341_no_madctl import Display

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


display = Display(spi, dc=Pin(dc), cs=Pin(cs), rst=Pin(rst), width=width, height=height, rotation=rotation)
