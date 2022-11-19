from machine import Pin, SPI
from .ili9341 import Display, color565
from .xglcd_font import XglcdFont

spi = SPI(2, baudrate=51200000, sck=Pin(18), mosi=Pin(23))
display = Display(spi, dc=Pin(2), cs=Pin(15), rst=Pin(4),width=240, height=320, rotation=270)
#display = Display(spi, dc=Pin(2), cs=Pin(15), rst=Pin(4),width=320, height=240, rotation=90)

red=color565(255, 0, 0)
black=color565(0, 0, 0)
white=color565(255,255,255)
drk_grn=color565(50,100,30)

score_font  = XglcdFont('../fonts/sb_21_27.c', 21, 27)
date_font   = XglcdFont('../fonts/arial_32_31.c', 32, 31)
sm_font  = XglcdFont('../fonts/arial_23_24.c', 23, 24)


if __name__ == "__main__":
    display.draw_text(0, 66, 'Espresso Dolce', score_font, drk_grn)
