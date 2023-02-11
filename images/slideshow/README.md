# BB-ESP32-KIOSK

#### ESP32 Game Day BaseBall Kiosk Slide Show

The BB-ESP32-Kiosk will go through several phases:

Booting Up and Launching, and Initialization:<P>
<img src="boot.jpg" width="200"/>
<img src="launch.jpg" width="200"/>

If it is during the regual season, BB-ESP32-Kiosk
will see if there is a game today. If so will show you one of 4 outcomes:<P>

1. Pregame. Games time will be show on the screen. Please Wait!<P>
<img src="pregame.jpg" width="200"/>

2. In Progress. (with current score, whose at bat, team records, pitch count, and inning status).<P>
<img src="progress.jpg" width="200"/>

BB-ESP32-KIOSK will refresh the score every 2 minutes.

3. Final Score. <P> 
<img src="final_score.jpg" width="200"/>
The final score will be shown with winning and losing pitchers, scores and records for 30 seconds. 
BB-ESP32-Kiosk will then  rotate through all the current news articles for the day  at mlb.com and the cycle is repeated.<P>

4. No Game. If there's no game, BB-ESP32-Kiosk will tell you:
<img src="nogame.jpg" width="200"/>
BB-ESP32-Kiosk will then  rotate through all the current news articles for the day  at mlb.com and the cycle is repeated.

<P>

If it is not during the regual season, BB-ESP32-Kiosk
will tell you when opening day is for 30 seconds:<P>
<img src="opening_day.jpg" width="200"/> <P>
BB-ESP32-Kiosk will then  rotate through all the current news articles for the day  at mlb.com and the cycle is repeated.

For example:<P>
<img src="news1.jpg" width="200"/>
<img src="news2.jpg" width="200"/>

This cycle will repeat infinitely.
