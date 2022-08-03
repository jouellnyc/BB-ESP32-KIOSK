# MLB-ESP32

#### Requirements

- ESP32 CAM
https://www.amazon.com/dp/B07WCFGMTF/
You can buy one with or with the ESP32-CAM-MB

- FT232RL FTDI Mini USB to TTL Serial Converter Adapter Module
https://www.amazon.com/HiLetgo-FT232RL-Converter-Adapter-Breakout/dp/B00IJXZQ7C

- Small Bread Board
https://www.amazon.com/Breadboard-Solderless-Prototype-PCB-Board

- Mini USB Cable

#### Steps

# Connect Esp-32 CAM (Bare) to FTDI 
# Connect Esp-32 CAM (Bare) to OLED

Using this setup, the FTDI supplies the power and allows for repl, if desired.

#### References 
PINS: https://stackoverflow.com/questions/71853347/interfacing-oled-to-esp32-cam
PIN CONNECT: https://randomnerdtutorials.com/program-upload-code-esp32-cam/
PIN MAP: https://randomnerdtutorials.com/esp32-cam-ai-thinker-pinout/
CODE: https://randomnerdtutorials.com/micropython-oled-display-esp32-esp8266/
API: https://github.com/toddrob99/MLB-StatsAPI

Connect USB / FTDI programmer to esp-cam as per the PIN CONNECT link.

And then connect esp32-cam to OLED:

esp32cam OLED
IO15     sda
IO13     scl

#### Code Setup


![ESP32-CAM-MLB-Kiosk](esp32-kiosk.png)


