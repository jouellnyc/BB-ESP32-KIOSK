# BB-ESP32-KIOSK
#### ESP32 Game Day BaseBall Kiosk


|<A HREF="https://www.tindie.com/products/lilygo/lilygo-ttgo-t4-v13-ili9341-24-inch-lcd-display/">LilyGo 2.4 Inch ili9341 ESP32</A> |<A HREF="https://www.aliexpress.us/item/3256802898629918.html">LilyGO T-WATCH-2020 V3 </A> |<A HREF="https://www.espressif.com/en/news/ESP32-S3-BOX_video">ESP32-S3-BOX Lite </A> |<A HREF="https://www.espressif.com/en/news/ESP32-S3-BOX_video">ESP32-S3-BOX</A>|
| ------------- | ------------- | ------------- |------------- |
|<img src="images/lily_24_esp32.png"  width="200"/>| <img src="images/lily_go_watch.png"  width="200"/>| <img src="images/esp-32-s3-box-lite.png" width="200"/>| <img src="images/esp_box.jpg" width="200"/>|


|<A HREF="https://www.thingiverse.com/thing:3461768"  >ThingVerse #1</A> |<A HREF="https://www.thingiverse.com/thing:3495445/files">ThingVerse #2 </A>|ESP32 on bread board with 2.8" Screen|
| ------------- | ------------- | ------------- | 
|<img src="images/side_view_black.jpg"    width="200"/>| <img src="images/orange.png" width="200"/>| <img src="images/esp32_plain.png"  width="200"/>|


- Build your own kiosk for your favorite baseball team:

  LilyGo Watch, LilyGo 2.4 ESP32, ESP32-S3-BOX/BoxLite, or ThingVerse Model using an ESP32 DevKit.  

- If it's gametime for your team, the kiosk will show the score every, including base runners:

   <img src="images/in_progress.jpg"   width="200"/>

  - then show any 'event' (hit/walk/timeout/homerun/etc):
   <img src="images/home_run.jpg"    width="200"/>

  - then show runners on base if they have changed:
   <img src="images/on_base.jpg"    width="200"/>
 
- If the game is over, it show you the final score:

   <img src="images/final.jpg"    width="200"/>

- If no game 'today', it will show you and and retry later:.

   <img src="images/no_game.jpg"    width="200"/>

- Afterwards, stories from mlb.com will display for 7 seconds and rotate:

   <img src="images/news.jpg"    width="200"/>

- If it's the offseason, it will tell you when open day is.

#### Requirements (if you are building your own)

- ESP32 DevKitC (or above hardware)
https://www.amazon.com/gp/product/B087TNPQCV/

- Mini USB or USB-C Cable
Anywhere cables are sold (short - 3 ft or less are best)

- 320x240 SPI Serial ILI9341 - https://www.amazon.com/dp/B09XHJ9KRX

- 2.4 GHZ WIFI SSID (esp hardware does not support 5 GHZ) 


#### Steps

- Install MicroPython with <A HREF="https://micropython.org/download/esp32spiram/">SPIRAM</A> to the ESP32:

- (For the LilyGo Watch use <A HREF="https://github.com/russhughes/st7789_mpy/tree/master/firmware/TWATCH-2020">this </A> firmware.)

- Get a REPL on the ESP32:

https://microcontrollerslab.com/getting-started-thonny-micropython-ide-esp32-esp8266/

- Install libraries 
```
git clone https://github.com/jouellnyc/BB-ESP32-KIOSK
 upload appsetup, bbbapp, hardware, fonts, and lib to / using Thonny/your IDE
 upload acknowledgements.py, main.py, boot.py and myugit.py to / using Thonny/IDE.
```

To connect the esp32 to an ili9341, you can follow https://www.youtube.com/watch?v=rq5yPJbX_uk

- edit the 'screen' variable in hardware/config.py to match your selected device/hardware:

#### Setup

Plug in BB-ESP32-KIOSK with a USB-C cable.

BB-ESP32-KIOSK will go through 3 stages:

- Booting up:
<img src="images/setup_boot.png" width="200"/>

- Running Setup:
<img src="images/setup_running.png" width="200"/>

- Setup Page:
<img src="images/setup_setup.png" width="200"/>


If you see the "Setup Page at" Screen, that means BB-ESP32-KIOSK  launched a temporary wifi SSID named 'bbkiosk32'.

The  password is '123456789'.

Connect your mobile phone/PC to that SSID using the password.

There will be no Internet Access via this ssid:

<img src="images/6_wifi.png" width="200"/>

Navigate your mobile phone/PC  to http://192.168.4.1

Enter the name of *your* Wifi SSID and password. 

<img src="images/1_setup.jpg" width="200"/>

On the same page, select your team from the drop down:

<img src="images/3_setup_team.jpg" width="200"/>

Click Submit (on the same page)

Click Reboot if Successful

<img src="images/4_setup_reboot.jpg" width="200"/>

The page will NOT Refresh (This is OK and expected):

<img src="images/5_setup_ok_no_connect.jpg" width="200"/>

(Connect back to Your Normal Wifi SSID to get your mobile/PC back online.)

The kiosk should boot and show startup mesages:

<img src="images/7_boot.jpg" width="200"/>

Once done, BBKiosk will display the status of Your Team's Game if in progress.

For more details of the flow of information see the <a href="https://github.com/jouellnyc/BB-ESP32-KIOSK/tree/main/images/slideshow">slideshow</A>.

### Upgrading Manually (without the ESP32-S3-BOX)
<img src="images/upgrade_off_host.png" width="200"/>


### Video
[Video -- BBKiosk in Action ](https://www.youtube.com/watch?v=aep2s7Il-oY)

### BreadBoard Version with OLEDs
Looking for the [BreadBoard Version with OLEDs](README.BREAD.BOARD.md) for the old school effect?

Code - https://github.com/jouellnyc/MLB-ESP32/tree/9bc62e9f47f77b68f4ae8cf7bbc0e8fba193373a
