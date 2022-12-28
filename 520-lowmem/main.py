import gc
import os

def show_mem():
        gc.collect()
        print(gc.mem_free())
    
def file_or_dir_exists(filename):
    try:
        os.stat(filename)
    except OSError:
        return False
    else:
        return True

mode='debug'

if mode=="normal":

    pass

else:

    if file_or_dir_exists('/appsetup/setup_complete.txt'):        

        """ NETWORK SETUP """
        import hardware.network_setup
        show_mem()

        """ NTP SETUP """
        import hardware.ntp_setup
        hardware.ntp_setup.main()
        show_mem()
        
        """ Run MLB APP """
        import mlbapp.mlb_app_runner
        show_mem()
        
    else:

        import appsetup.setup