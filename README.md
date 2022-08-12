# MLB-ESP32

#### ESP32 CAM MLB Mini Kiosk
|<img src="images/esp32-kiosk.png"  width="200"/>|<img src="images/esp32-kiosk-live.png" width="200"/>|<img
src="images/esp32-kiosk.over.png" width="200"/>|

#### What 
- Build your own MLB team kiosk  for your favorite team on a tiny device - all in for $15 or less...
- If it's gametime the kiosk will refresh every 120 seconds
- If no game it will wait a few hours and retry
- Only 1 Network Request is needed per update to https://statsapi.mlb.com/. 

#### Requirements

- ESP32 CAM
https://www.amazon.com/dp/B07WCFGMTF/

  You can buy one with or with the ESP32-CAM-MB. These boards typically have 4 MB of spiram.

  see https://micropython.org/download/esp32spiram/ for the right firmware.

  This repo is unlikely to work on a ESP8266 based board w/o modifications, hence the use of a 4 MB board. 

  The difference in dollar cost is minimal, but code effort is likely much larger.

- FT232RL FTDI Mini USB to TTL Serial Converter Adapter Module

  https://www.amazon.com/HiLetgo-FT232RL-Converter-Adapter-Breakout/dp/B00IJXZQ7C

- Small Bread Board

  https://www.amazon.com/Breadboard-Solderless-Prototype-PCB-Board

- Mini USB Cable
  Anywhere Mini usb cables are sold
 
- API: https://github.com/toddrob99/MLB-StatsAPI 
  (Modified here - my_mlb_api.py was renamed from __init__.py in MLB-StatsApI and just barely modified.


#### Steps

Using this setup, the FTDI supplies the power and allows for repl, if desired.

- Connect USB FTDI programmer to esp-cam as per the PIN CONNECT link in References.

- Connect Esp-32 CAM (Bare) to OLED with male to male jumpers:

| Esp32cam       | OLED          |
| :-------------:|:-------------:|
| IO15           | sda           |
| IO13           | sdcl          |


- Install MicroPython with SPIRAM to the ESP32:
- Get a REPL on the ESP32:
https://microcontrollerslab.com/getting-started-thonny-micropython-ide-esp32-esp8266/

- Edit the Wifi Config:
```
vi net_config.py  #should be obvious
```

- Edit tm_id = XXX and set to your team's id 
```
vi  mlb_app_runner.py 
```

- Upload mlbapp/ folder using Thonny/IDE as well as:
```
- boot.py 
- main.py
```

- Install 2 Libraries
```
import upip
upip.install('urequests')
upip.install('micropython-logging')
```

Note: ssd1306.py is from https://github.com/micropython/micropython/blob/master/drivers/display/ssd1306.py

to '/'

#### References 

- PINS: https://stackoverflow.com/questions/71853347/interfacing-oled-to-esp32-cam
- PIN CONNECT: https://randomnerdtutorials.com/program-upload-code-esp32-cam/
- IN MAP: https://randomnerdtutorials.com/esp32-cam-ai-thinker-pinout/
- OLED SETUP CODE: https://randomnerdtutorials.com/micropython-oled-display-esp32-esp8266/

#### TBD
- Make the code better post current MicroPythonic issues
- Using Scrolling for more information on the kiosk
- Implement Push Button for Real Time update
