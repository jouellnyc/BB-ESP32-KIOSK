"""

# Pico to Uctronics I2C OLED screen 128 x 64
# https://www.tomshardware.com/how-to/oled-display-raspberry-pi-pico

1. Connect the GND of the OLED screen to any GND on the Pico (Black wire).
2. Connect VDD / VCC to 3V3 on the Pico (Red wire).
3. Connect SCK / SCL to I2C0 SCL (GP1, Physical pin 2, Orange wire).
4. Connect SDA to I2C0 SDA (GP0, Physical pin 1, Yellow wire).

pico pins map
https://www.theengineeringprojects.com/wp-content/webp/2021/03/what-is-raspberry-pi-pico.png.webp?ssl=1

"""

from machine import Pin,I2C
from . import ssd1306
#0th or first i2c bus
i2c = I2C(0,sda=Pin(0), scl=Pin(1), freq=400000)
oled=ssd1306.SSD1306_I2C(128,64,i2c) #create oled object,Specify col and row
oled.fill(0)
oled.show()
oled.text("hello",0,0)
oled.show()


