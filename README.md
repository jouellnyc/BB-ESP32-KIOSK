# BB-ESP32-KIOSK

#### ESP32 Game Day BaseBall Kiosk


|<A HREF="https://www.tindie.com/products/lilygo/lilygo-ttgo-t4-v13-ili9341-24-inch-lcd-display/">LilyGo 2.4 Inch ili9341 ESP32</A> 
|<A HREF="https://www.aliexpress.us/item/3256802898629918.html">LilyGO T-WATCH-2020 V3 </A> 
|<A HREF="https://www.espressif.com/en/news/ESP32-S3-BOX_video">ESP32-S3-BOX Lite</A>
|<A HREF="https://www.thingiverse.com/thing:3461768">ThingVerse #1</A> 
|<A HREF="https://www.thingiverse.com/thing:3495445/files">ThingVerse  #2|
| ------------- | ------------- | ------------- | ------------- | -------------|
|<img src="images/lily_24_esp32.png"      width="200"/>|
 <img src="images/lily_go_watch.png"      width="200"/>|
 <img src="images/esp-32-s3-box-lite.png" width="200"/>|
 <img src="images/side_view_black.jpg"    width="200"/>|
 <img src="images/orange.png"             width="200"/>|

#### What 
- Build your own kiosk for your favorite baseball team:

  LilyGo Watch, LilyGo 2.4 ESP32 or ThingVerse Model using an ESP32 DevKit.  
- If it's gametime the kiosk will refresh every 120 seconds.
- If no game 'today',  it will wait a few hours and retry.


#### Requirements
- ESP32 DevKitC
https://www.amazon.com/gp/product/B087TNPQCV/

- Mini USB Cable
Anywhere Mini usb cables are sold (short - 3 ft or less are best)

- 320x240 SPI Serial ILI9341 - https://www.amazon.com/dp/B09XHJ9KRX

- Configs / Libraries shared in https://github.com/jouellnyc/mcconfigs 



#### Steps

- Install MicroPython with <A HREF="https://micropython.org/download/esp32spiram/">SPIRAM</A> to the ESP32:
- (For the LilyGo Watch use <A HREF="https://github.com/russhughes/st7789_mpy/tree/master/firmware/TWATCH-2020">this </A> firmware.)

- Get a REPL on the ESP32:

https://microcontrollerslab.com/getting-started-thonny-micropython-ide-esp32-esp8266/

- Install libraries 
```
git clone https://github.com/jouellnyc/MLB-ESP32
 upload appsetup, bbbapp, main.py and boot.py to / using Thonny/your IDE
git clone https://github.com/jouellnyc/mcconfigs
 upload fonts, hardware, and lib to / using Thonny/your IDE
```

To connect the esp32 to an ili9341, you can follow https://www.youtube.com/watch?v=rq5yPJbX_uk

#### Setup
At boot the esp32 launches a wifi SSID named 'bbkiosk32' and a password of '123456789'.

Connect your mobile phone/PC w/wifi to that SSID.

There will be no Internet Access via this ssid:

<img src="images/6_wifi.png" width="200"/>

Navigate to http://192.168.4.1

Enter your local Wifi SSID, Credentials: 

<img src="images/1_setup.jpg" width="200"/>

On the same page, select your team from the drop down:

<img src="images/3_setup_team.jpg" width="200"/>

Click Submit (on the same page)

Click Reboot if Successful

<img src="images/4_setup_reboot.jpg" width="200"/>

The page will NOT Refesh (This is OK and expected):

<img src="images/5_setup_ok_no_connect.jpg" width="200"/>

(Connect back to Your Normal Wifi SSID to get your mobile/PC back online.)

The kiosk should boot and show startup mesages:

<img src="images/7_boot.jpg" width="200"/>

Once Done, it will show you status of Your Team's Game if in progress.

### BreadBoard Version with OLEDs
Looking for the [BreadBoard Version with OLEDs](README.BREAD.BOARD.md) for the old school effect?

Code - https://github.com/jouellnyc/MLB-ESP32/tree/9bc62e9f47f77b68f4ae8cf7bbc0e8fba193373a
