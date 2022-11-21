# MLB-ESP32

#### ESP32 CAM MLB Mini Kiosk

|<img src="images/esp32-kiosk.png"  width="200"/>|<img src="images/esp32-kiosk-live.png" width="200"/>|<img src="images/esp32-kiosk.over.png" width="200"/>|

Possible ThingVerse Option #1 (uses code for esp32-ili9341-2.8)
|<img src="images/side_view_black.jpg" width="200"/>

Possible ThingVerse Option #2 (uses code for esp32-ili9341-2.8)
|<img src="images/orange.png" width="200"/>|

#### What 
- Build your own MLB team kiosk  for your favorite team on a tiny device - all in for $15 or less...
- If it's gametime the kiosk will refresh every 120 seconds.
- If no game it will wait a few hours and retry.
- RGB LED (optional) turns RED if your team is losing, GREEN if winning, BLUE if a tie or WHITE if a game is scheduled for later.
- Only 1 Network Request is needed per update to https://statsapi.mlb.com/. 

#### Requirements

- ESP32 CAM
https://www.amazon.com/dp/B07WCFGMTF/

  You can buy one with or with the ESP32-CAM-MB. These boards typically have 4 MB of spiram.

  see https://micropython.org/download/esp32spiram/ for the right firmware.

  This repo is unlikely to work on a ESP8266 based board w/o modifications due to RAM usage, I chose the 4 MB board to
  have plenty. 

  The difference in dollar cost is minimal, but code effort is likely much larger.

- FT232RL FTDI Mini USB to TTL Serial Converter Adapter Module

  https://www.amazon.com/HiLetgo-FT232RL-Converter-Adapter-Breakout/dp/B00IJXZQ7C

- (Optional) "Breadboard Power Supply Board Module 3.3V/5V Dual Voltage (2 Pack) by MakerSpot"
  If you want the power supply to lay flat vs standing up like the FTDI, you can use this:
  https://www.amazon.com/gp/product/B08KQ9DNQZ/

  NOTE1: it won't allow you connect to the ESP32-cam over usb to upload files.

  NOTE2: Both this power supply and the FTDI have a slighltly annoying RED LED that's on if it's power is on.

- (Optional) "ESP32-CAM-CH340" - ESP32-CAM with built mini usb that is Breadboard friendly:
  I have really only seen these on ebay: https://www.ebay.com/itm/185476432256. This will not have the RED LED and gets
  power from the mini usb.

- Small Bread Board

  https://www.amazon.com/Breadboard-Solderless-Prototype-PCB-Board

- Mini USB Cable
  Anywhere Mini usb cables are sold
 
- API: https://github.com/toddrob99/MLB-StatsAPI 
  (Modified here - my_mlb_api.py was renamed from __init__.py in MLB-StatsApI and just barely modified.

- (For ThingiVerse Large Screen Setup) - 320x240 SPI Serial ILI9341 - https://www.amazon.com/dp/B09XHJ9KRX


#### Steps

Using this setup, the FTDI supplies the power and allows for repl, if desired.

- Connect USB FTDI programmer to esp-cam as per the PIN CONNECT link in References.

- Connect Esp-32 CAM (Bare) to OLED with male to male jumpers:

| Esp32cam       | OLED          |
| :-------------:|:-------------:|
| IO15           | sda           |
| IO13           | sdcl          |


- Connect Esp-32 CAM to the RGB LED (optional) :

There are many pics online to  to understand how to setup the reisistor to the RGB:
* https://github.com/danielwohlgemuth/blinking-led-micropython-esp32
* https://learn.sparkfun.com/tutorials/getting-started-with-micropython-and-the-sparkfun-inventors-kit-for-microbit/experiment-4-driving-an-rgb-led
* https://microcontrollerslab.com/esp32-rgb-led-web-server/
* https://microcontrollerslab.com/micropython-pwm-with-esp32-and-esp8266-led-fading-brightness-control-examples/

You can try 200 Ohm resistors, or higher depending on the LED.
I have about 500 Ohms using 2 resistors in series, because that's what I had available at the time.


However, you will be using PINS 12, 2, and 14 for the red, blue, and green legs of the LED respectively. 

This is reflected in rgb.py: 

```
r = Pin(12, Pin.OUT)
g = Pin(2, Pin.OUT)
b = Pin(14, Pin.OUT)
```

You can place the RGB LED in the breadboard in any manner, there is no forward or backwards, but if you count the legs from left to right as 1, 2, 3, 4, I connected
them like this:

| Esp32cam       | RGB LED       |What      |
| :-------------:|:-------------:|:--------:|
| IO14           | 1             | Blue leg |
| IO02           | 2             | Green leg|
| GRND           | 3 longest leg | Ground   |
| IO12           | 4 (furthest to the right)| Red Leg|

Yes, the esp32 cam is very crowded now and is almost using 'all available' GPIOs.

<img src="images/esp32-kiosk-RGB-won.png" width="200"/>

But you have visual and don't need to read the screen anymore...


- Install MicroPython with SPIRAM to the ESP32:
- Get a REPL on the ESP32:

https://microcontrollerslab.com/getting-started-thonny-micropython-ide-esp32-esp8266/

- Edit the Wifi Config:
```
vi net_config.py  #should be obvious
```

- Edit tm_id = XXX and set to your team's id 
```
edit the mlb_app_runner.py  file
```

- Upload the mlbapp/ and  lib/ folder using Thonny/IDE as well as:

```
- boot.py 
- main.py
```

to '/'


Note: ssd1306.py is from https://github.com/micropython/micropython/blob/master/drivers/display/ssd1306.py


When expanded the view from Thonny should look like this:

<img src="images/thonny.png"  width="200"/>


#### References 

- PINS: https://stackoverflow.com/questions/71853347/interfacing-oled-to-esp32-cam
- PIN CONNECT: https://randomnerdtutorials.com/program-upload-code-esp32-cam/
- IN MAP: https://randomnerdtutorials.com/esp32-cam-ai-thinker-pinout/
- OLED SETUP CODE: https://randomnerdtutorials.com/micropython-oled-display-esp32-esp8266/

Black Case:
- https://www.thingiverse.com/thing:3495445/files

Orange Case:
- https://www.thingiverse.com/thing:3461768

