#!/bin/bash

set -e
set -u 

cd /home/jouell/gitrepos/MLB-esp32
FILE=mlb.$(date +%F).tar
tar --exclude-vcs  -cvf  $FILE  mlbapp
mv $FILE  ~/esp32/bak/
cp -pvr ~/esp32/ghtemp/mlb_proj/mlbapp/ .
cp wifi_config.py mlbapp/wifi_config.py
