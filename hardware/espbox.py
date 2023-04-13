""" These value are for the ESP32-S3-BOX """
from machine import Pin, SPI, ADC
import time

from .ili9341 import color565, Display

from .font_runner import sm_font, score_font, date_font
from bbapp.version import version

drk_grn=color565(58, 124, 14)   # esp full box
black=color565(0, 0, 0)
white=color565(255,255,255)
yellow=color565(255, 0, 0)
green=color565(0,0,255)
pink=color565(0, 255, 0)

dc=4
cs=5
rst=48
rotation=0
width=320
height=240

spi = SPI(1, baudrate=40000000, sck=Pin(7), mosi=Pin(6))
display = Display(spi, dc=Pin(dc), cs=Pin(cs), rst=Pin(rst), width=width, height=height, rotation=rotation)

adc = ADC(Pin(1))



""" How many chars per line  before you hit the end """
anum = {'r': '36', 'Y': '19', 'Z': '22', 'y': '27', 'x': '27', 'z': '27', 'E':'21',
        'D': '19', 'G': '18', 'F': '22', 'A': '21', 'C': '19', 'B': '21', 'M':'18',
        'L': '25', 'O': '17', 'N': '21', 'I': '65', 'H': '21', 'K': '19', 'J': '30',
        'U': '21', 'T': '22', 'W': '14', 'V': '21', 'Q': '17', 'P': '21', 'S': '21',
        'R': '19', 'e': '25', 'd': '25', 'g': '25', 'f': '41', 'a': '25', 'X': '21',
        'c': '27', 'b': '23', 'm': '17', 'l': '65', 'o': '25', 'n': '25', 'i': '65',
        'h': '25', 'k': '25', 'j': '65', 'u': '25', 't': '41', 'w': '18', 'v': '27',
        'q': '25', 'p': '23', 's': '27'}

""" How many pixels/char, rounded up (/320) """
apnt3 = {'.':10, 0:13, 1:10, 2:13, 3:13, 4:13, 5:13, 6:13, 7:13, 8:13, 9:13, '-':12,
        "'":5, ' ': 19, 'r': 8, 'X': 15, 'Z': 14, 'y': 11, 'x': 11, 'z': 11,
        'E': 15, 'D': 16, 'G': 17, 'F': 14, 'A': 15, 'C': 16, 'B': 15, 'M': 17,
        'L': 12, 'O': 18, 'N': 15, 'I': 4, 'H': 15, 'K': 16, 'J': 10, 'U': 15,
        'T': 14, 'W': 22, 'V': 15, 'Q': 18, 'P': 15, 'S': 15, 'R': 16, 'e': 12,
        'd': 12, 'g': 12, 'f': 7, 'Y': 16, 'a': 12, 'c': 11, 'b': 13, 'm': 18,
        'l': 4, 'o': 12, 'n': 12, 'i': 4, 'h': 12, 'k': 12, 'j': 4, 'u': 12,
        't': 7, 'w': 17, 'v': 11, 'q': 12, 'p': 13, 's': 11}

""" How many pixels/char, rounded up (/240) """
apnt2 = {'K': 18, 'J': 11, 'U': 15, 'T': 15, 'W': 22, 'V': 16, 'Q': 19, 'P': 15,
         'S': 15, 'R': 16, 'Z': 15, 'Y': 16, 'E': 15, 'D': 18, 'G': 18, 'F': 15,
         'A': 16, 'X': 16, 'C': 18, 'B': 15, 'M': 19, 'L': 14, 'O': 19, 'N': 15,
         'I': 6, 'H': 15, 't': 7, 'w': 18, 'v': 12, 'q': 12, 'p': 13, 's': 12,
         'r': 9, 'z': 11, 'y': 12, 'e': 13, 'd': 12, 'g': 12, 'f': 8, 'a': 13,
         'x': 11, 'c': 12, 'b': 13, 'm': 19, 'l': 5, 'o': 13, 'n': 13, 'i': 5,
         'h': 13, 'k': 13, 'j': 5, 'u': 13, 0: 14, 1: 10, 2: 13, 3: 14, 4: 14,
          5:14, 6: 14, 7: 14, 8: 14, 9: 14, "'": 4, '-': 8, ' ': 14, '.': 6}

def draw_outline_box():
    display.draw_vline(0,    0, 240, white)
    display.draw_vline(319,  0, 240, white)
    display.draw_hline(0,    0, 320, white)
    display.draw_hline(0,   40, 320, white)
    display.draw_hline(0,  239, 320, white)
    
def clear_fill():
    display.clear()
    display.fill_rectangle(0,0, 320, 240, drk_grn)
    
def fresh_box():
    display.clear_fill()
    display.draw_outline_box()

def print_setup(boot_stage):
    clear_fill()    
    draw_outline_box()
    display.draw_text(5, 8,  f"{boot_stage}"       , date_font, white, drk_grn)
    display.draw_text(5, 65, 'BB Kiosk'            , date_font, white, drk_grn)
    display.draw_text(5, 105, f"Version {version}" , date_font, white, drk_grn)

def crash_burn(err):
    display.fresh_box()
    print(f"=={err}")
    display.draw_text(5, 5, err, date_font, white, drk_grn)
    time.sleep(5)
    import machine
    machine.reset()

def get_tb_text(err):
    """
    Credit https://forums.openmv.io/t/how-can-i-get-the-line-number-of-error/6145
    """
    import io
    import sys
    buf = io.StringIO()
    sys.print_exception(err, buf)
    #Remove the word Traceback/etc
    print(buf.getvalue()[35:])
    return buf.getvalue()[35:]
    
def scroll_print(text='NA',x_pos=5, y_pos=5, scr_len=30,
                 Error=False, clear=True, font=sm_font,
                 bg=drk_grn, fg=white, debug=False):
    """ Given a headline from a text string from mlb.com/news like:

       'Celebrate Aaron's birthday with 13 stats that show his greatness'
        
       We need to break it into grouping like this:
       
       ["Celebrate Aaron's", 'birthday with 13', 'stats that show his', 'greatness']
       
       ...but do so in a way that does not step outside the character/pixel limits  
         
       We  pass in a 'text container' to scroll_print which will be either
       and instance of an error or a string                                        """
    
    debug = True
    
    if clear:
        display.fresh_box()        
    
    """ 5 is already tight, 6 partly off the screen """
    max_rows = 6
    scr_len  = scr_len
        
    def proc_text(text):
        """ Here's where we do the processing of the 'text' """
        
        def get_raw_parts(_text):
            """ Split 'text' to list[] in scr_len increments as a first pass
            return a list of 'raw' parts like this:
            ["Celebrate Aaron's", "birthday with 13 s","tats that show his greatness"] """
            return [ _text[i:i + scr_len]
                     for i in range(0,len(_text),scr_len)
                         if any([ x.isalpha() for x in _text[i:i + scr_len]])
                   ]
                
        def mv_parts(text):
            """ Cycle through / Get the 'raw' 'parts' of  'text', convert each to a list.
                Then align() each item/push characters to the next part if needed. 
                
                Return a list of strings that do not 'run on', but still need to be processed for length.
                Ex. ["Celebrate Aaron's ", 'birthday with 13 ', 'stats that show his', ' greatness']   """
            
            print(f"Text: {text}") if debug else None
            raw_parts = get_raw_parts(text)
            print (f"len() raw_parts: {len(raw_parts)}") if debug else None
            print(f"Raw Parts: {raw_parts}") if debug else None
            
            if debug:
                for idx, _each in enumerate(raw_parts):
                    print(f"Raw Part {idx}: {_each} -  Raw tsum: {get_tsum(_each)}")  
            
            max_num_raw_parts = len(raw_parts)-2
            start=0
            while start <= max_num_raw_parts:
                """Convert Text parts to lists to be able to pop easily """
                t1=list(raw_parts[start])
                t2=list(raw_parts[start+1])
                """ Move upstream through raw_parts align()ing to a new list as you go """
                raw_parts[start], raw_parts[start+1] = align(t1,t2)
                print(f"Parts after round {start} {raw_parts}") if debug else None
                start+=1
            return raw_parts
        
        def align(_t1, _t2):
            """ Given the first 2 portions of the text converted to lists,
                see if the end of the 1st list and the start of the 2nd list are
                alphanumeric, if so push text to avoid a broken word on the screen
                
                Ex.
                ['W', 'h', 'i', 't', 'e', 'S']['o', 'x', ' ', 'a', 'c', 'q', 'u', 'i', 'r', 'e']
                to 
                ['W', 'h', 'i', 't', 'e']['S','o', 'x', ' ', 'a', 'c', 'q', 'u', 'i', 'r', 'e']
                
                then return a tuple of strings:
                
                
                """
            if run_on(_t1, _t2):
                _t2.insert(0,_t1.pop(-1))                                                                                                                                                     
                _t1, _t2 = align(_t1,_t2)
            return ''.join(_t1), ''.join(_t2)
            
        
        def run_on(_t1, _t2):
            """ check for align() """
            if _t1[-1] != ' ' and _t2[0] != ' ':
                return True
            return False
        
            
        def get_tsum(thing, def_size=15):
            """ Given the footprint of each character, return the sum(), "tsum" of it
                whether it's a string or a list, to determine how to postion the text """
            if isinstance(thing, list):
                return sum([ apnt2.get(x,def_size) for x in ' '.join(thing)])
            if isinstance(thing, str):
                return sum([ apnt2.get(x,def_size) for x in thing ])
        
        def rm_space(_parts):
            """ rm final / inital spaces of each part of given list """
            [ x.pop()  for x in _parts if x[-1] == ' ' ]
            [ x.pop(0) for x in _parts if x[0]  == ' ' ]
            return _parts
            
        def sw_parts(parts):
            """ Swap parts like
                from ['One series to ', "circle on each team's ", "schedule in '23"  ]
                to
                     ['One series to ', "circle on each  ", " team's schedule in '23"]
                if their pixel footprint (tsum) breaks past the screen's max           """
            
            def bump(each, tsum):
                """ Insert strategically into a list (push to a non existing 'part'/list to create it)
                    for the last 'each', or into an (already existing 'each'/list) inside a list         """
                if tsum > max_x:
                    print(f"over {max_x}") if debug else None
                    if len(_pparts) == each+1:
                        _pparts.insert(each+1,[_pparts[each].pop(-1)])
                    else:
                        _pparts[each+1].insert(0,_pparts[each].pop(-1))
                    tsum = get_tsum(_pparts[each])
                    print(f"New _pparts each {_pparts[each]} new tsum {tsum}") if debug else None
                    bump(each, tsum)
                
            """ Given the aligned parts(strings), convert each to list to rm space easily """
            _parts = [ list(x) for x in parts ]
            print(f"_parts list comp {_parts}") if debug else None
            
            """ There is no need for beg/end spaces at all right now, rm them """
            _parts = rm_space(_parts)
            print(f"_parts list rm_space {_parts}") if debug else None
            
            """ join them all back to get words back """
            _parts = [ ''.join(x) for x in _parts ]
            print(f"_parts Current joined  {_parts}") if debug else None
            
            """ make each part a list in a new candidate list for easy bumping of a full word/string """
            _pparts = [ x.split(' ') for x in _parts ]
            print(f"_pparts Current list cand to bump {_pparts}") if debug else None
            print(f"lp {len(_parts)}") if debug else None
            
            max_x=230
            
            for each in range(0, len(_parts)):
                if debug:        
                    print(f"---- Each {each}") 
                    print(f"-- each _parts  {each}: {_parts[each]}  {  get_tsum(_parts[each]) }") 
                    print(f"-- each _pparts {each}: {_pparts[each]} { get_tsum(_pparts[each]) }") 
                bump(each, get_tsum(_pparts[each]))              
            
            print(f"Final swapped but unjoined _pparts {_pparts}") if debug else None
            if debug:
                for each in _pparts:
                    print(get_tsum(each)) 
               
            _parts = [ ' '.join(x) for x in _pparts ]
            print(f"Final joined _parts {_parts}") if debug else None
            if debug:
                for each in _parts:
                    print(get_tsum(each)) if debug else None
                
            return _parts
        
        return sw_parts(mv_parts(text))
    
    """ If an error instance, pull out the text other process the beast ...   """

    if Error:
        
        _text = get_tb_text(text)
        print(f"_text: {text} type: {type(_text)}, len: {len(_text)}") if debug else None
        procd_parts =   [ _text[-150:-125], _text[-125:-100],
                          _text[-100:-75],   _text[-75:-50],
                          _text[-50:-25],    _text[-25:-1] ]
    else:
        
        procd_parts = proc_text(text)
    
    
    print(f"Final procd_parts parts {procd_parts}") if debug else None

    count=0
    for each_text in procd_parts:
        """ sm font = 25, date font =30  """
        if count > max_rows:
            break
        else:
            display.draw_text(x_pos, y_pos, each_text, font=font, color=fg,  background=bg)
            print(f"{each_text}") #This will be each story or the error message
        count+=1
        y_pos+=30


def check_upgrade():
    """ We only check the Mute Button on the ESP BOX - It's on GPIO01
    #Unpushed:
    >>>adc.read_u16()
    65535
    
    #Pushed
    >>> adc.read_u16()
    0
    """
    if adc.read_u16() == 0:
        return True

display.draw_outline_box = draw_outline_box
display.clear_fill       = clear_fill
display.print_setup      = print_setup
display.white            = white
display.drk_grn          = drk_grn
display.black            = black
display.sm_font          = sm_font
display.score_font       = score_font
display.date_font        = date_font
display.get_tb_text      = get_tb_text
display.scroll_print     = scroll_print
display.check_upgrade    = check_upgrade
display.fresh_box        = fresh_box
display.crash_burn       = crash_burn
