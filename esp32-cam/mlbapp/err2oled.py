def printout(string,oled):
    
    md={}
    
    #Vertical start point to Write to the oled
    depth=0
    #Fixed Horizontal point to Write to the oled
    horiz=0
    #Max Number of Rows
    max_rows=7
    
    num_rows = -(-len(string) // 16)
    scr_len = const(16)
    
    #Here we try to fill up all of the rows
    for x in range(1,num_rows+1):
        if x > max_rows:
            break
        else:
            start = (x - 1)  * scr_len 
            end= x * scr_len
            x='row' + str(x)
            oled.text(string[start:end],horiz,depth)
        depth+=9

