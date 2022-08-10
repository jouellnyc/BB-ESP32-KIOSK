import time

""" NETWORK SETUP """
import mlbapp.network_setup

""" NTP SETUP """
import mlbapp.ntp_setup
mlbapp.ntp_setup.main()

""" Run MLB APP """
import mlbapp.mlb_app_runner.py
