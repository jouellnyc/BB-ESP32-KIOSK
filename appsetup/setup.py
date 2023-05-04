from hardware.screen_runner import display as d

try:
    
    import time
    import network
    essid="bbkiosk32"
    ap = network.WLAN(network.AP_IF)
    ap.config(essid=essid, password='123456789')
    ap.active(True)
    # The system completely blows up
    # without  enough sleep after setting up 'ap'
    time.sleep(5)

    ip_addr = ap.ifconfig()[0]

    from hardware.config import screen, gui_screen_types 

    if screen in gui_screen_types:
        
        d.clear_fill()
        d.draw_outline_box()
        d.draw_text(5, 5,  'Setup Page at',            d.date_font,  d.white , d.drk_grn)
        d.draw_text(5, 65,  f"http://{ip_addr}",       d.date_font,  d.white , d.drk_grn)
        d.draw_text(5, 125, "Wifi ssid:", d.score_font, d.white, d.drk_grn)
        d.draw_text(5, 165, f"{essid}",                d.score_font, d.white , d.drk_grn)

    elif screen == 'oled':
        
        d.text('Setup at '  ,0,0)
        d.text("http://", 0, 17)
        d.text(f"{ip_addr}" ,0,34)
        d.show()

    """ INITIAL SETUP """
    from . import microdot_runner


except Exception as e:
    """ Dump to the screen """
    print(e)
    d.scroll_print(text=e, scr_len=30, Error=True)    