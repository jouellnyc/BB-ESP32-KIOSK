""" NTP - Setup
    We set the local time via ntp because we do not trust the device to store time
    ntpsettime does not support timezones, it defaults to UTC
"""

def main():
    
    import time
    import ntptime
    print("Local time before synchronization：%s" % str(time.localtime()))
    """ Thing can hang for a really long time if DNS is not working """
    """ https://github.com/micropython/micropython/issues/7137      """
    ntptime.host = "time.google.com"

    ntp_count=0
    while True:
        try:
            # This sets the RTC to UTC.
            ntptime.settime()
        except OSError as e:
            if 'ETIMEDOUT' in str(e):
                print('NTP timeout, retrying')
                ntp_count+=1
                print(f"NTP retry count {ntp_count}")
                time.sleep(1)
                if ntp_count > 4:
                    print("Fatal NTP Error")
                    import machine
                    machine.reset()
        else:
            print("Set Time to UTC")
            print("Local time after synchronization：%s" % str(time.localtime()))
            break
    
if __name__ == "__main__":
    
    main()    
    