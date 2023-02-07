       
from hardware.screen_runner import display as d
from hardware.ili9341 import AA

d.clear_fill()
d.draw_outline_box()

u_alphabet = [chr(i) for i in range(ord('a'.upper()), ord('z'.upper())+1)]
l_alphabet = [chr(i) for i in range(ord('a'), ord('z')+1)]
nums = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, '.', '-', "'", ' ',]

ml={}
for y in nums: 

    count=1
    for x in range(1,150):
        story= str(y) * x
        try:
            d.draw_text(0, 0, story, font=d.date_font, color=d.white, background=d.drk_grn)
            #print(f"OK {count}")
        except AA:
            import math
            print(f"{y}:{math.ceil(240/count)}")
            ml[y] = math.ceil(240/count)
            break
        finally:
            count+=1        
print(ml)
            
            

