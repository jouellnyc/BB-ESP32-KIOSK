# MLB-ESP32

#### What 
- Build you own MLB team kiosk  for your favorite team on a tiny device - all in for $15 or less...
- If it's gametime the kiosk will refresh every 60 seconds
- If no game it will wait a few hours and retry
- Only 1 Network Request is needed per update to https://statsapi.mlb.com/. 

#### Requirements

- ESP32 CAM
https://www.amazon.com/dp/B07WCFGMTF/

  You can buy one with or with the ESP32-CAM-MB. These boards typically have 4 MB of spiram.

  see https://micropython.org/download/esp32spiram/ for the right firmware.

  This repo is unlikely to work on a ESP8266 based board w/o modifications, hence the use of a 4 MB board. 
  The difference in cost is minimal.

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


- Install MicroPython:
https://microcontrollerslab.com/getting-started-thonny-micropython-ide-esp32-esp8266/

- Install 2 Libraries

```
import upip
upip.install('urequests')
upip.install('micropython-logging')
```

- Edit the Wifi Config:
```
vi network_setup.py #should be obvious
```

- Upload 

```
- statsapi (folder) (keep endpoints.py  in here)
- ssd1306.py
- team_ids.py
- network_setup.py
- my_mlb_api.py
- myoled.py
- boot.py 
```
ssd1306.py is from https://github.com/micropython/micropython/blob/master/drivers/display/ssd1306.py

to '/'

#### Picture of the mini Kiosk
![ESP32-CAM-MLB-Kiosk](esp32-kiosk.png)

#### References 

- PINS: https://stackoverflow.com/questions/71853347/interfacing-oled-to-esp32-cam
- PIN CONNECT: https://randomnerdtutorials.com/program-upload-code-esp32-cam/
- IN MAP: https://randomnerdtutorials.com/esp32-cam-ai-thinker-pinout/
- OLED SETUP CODE: https://randomnerdtutorials.com/micropython-oled-display-esp32-esp8266/

#### TBD
- Figure out how to get a clearer Picture of the Kiosk
- Make the code better
- Using Scrolling for more information on the kiosk
- Implement Push Button for Real Time update
- Overcome UTC challenges

#### Caveats
UTC is big pain on micropython, I intentionally rely on NOT using NTP, which make dates much simpler.
