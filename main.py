import os
import mlbapp.esp32cam_oled as myoled 
import mlbapp.err2oled


def file_or_dir_exists(filename):
    try:
        os.stat(filename)
    except OSError:
        return False
    else:
        return True

try:

    if file_or_dir_exists('/appsetup/setup_complete.txt'):        


        """ NETWORK SETUP """
        import mlbapp.network_setup

        """ NTP SETUP """
        import mlbapp.ntp_setup
        mlbapp.ntp_setup.main()
        
        """ Run MLB APP """
        import mlbapp.mlb_app_runner.py


    else:

        import appsetup.setup.py

except Exception as e:
    mlbapp.err2oled.printout(str(e),myoled.oled)
    myoled.oled.show()
    