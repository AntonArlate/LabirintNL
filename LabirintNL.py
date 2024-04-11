import time
from tkinter import *

m_width=600
m_height=600
room_w=500
room_h=500
shift=50
scale=20
x=100
y=205
step=10
wall_color="red"
item_color="yellow"
background_color1="pink"
background_color2="orange"

tk=Tk()#window
tk.title("Title")#its title
tk.resizable(0,0)# cannot resize
#tk.wm_attributes("-tompost",1)#overlape


canvas=Canvas(tk,width=m_width,height=m_height,bd=0,highlightthickness=0)#окно, его ширина, высота, толщина границ
canvas.pack()
tk.update()

def paintItem():
    global canvas
    global x
    global y
    global wall_color
    ##canvas.create_rectangle(x*scale,y*scale,x*scale+scale,y*scale+scale,fill=wall_color)
    canvas.create_oval(x,y,x+scale,y+scale,fill=wall_color)
paintItem()




flagX=True
flagY=True
def move():
    global x
    global y
    global m_width
    global m_height
    global flagX
    global flagY
    if flagX:
        if x<room_w-scale:
           x+=step
        else:
           flagX=False
    else:
        if x>shift:
           x-=step
        else:
           flagX=True

    if flagY:
        if y<room_h-scale:
           y+=step
        else:
           flagY=False
    else:
        if y>shift:
           y-=step
        else:
           flagY=True
    

while 1: 
    
    canvas.create_rectangle(0,0,m_width,m_height,fill=background_color1)
    canvas.create_line(
       room_w/2-scale/2,shift,
       shift,shift,
       shift,room_h,
       room_w,room_h,
       room_w,shift,
       room_w/2+scale/2,shift,
       fill="black",
       width=2)
    ##canvas.create_rectangle(shift,shift,room_w,room_h,fill=background_color2)
    #move()
    paintItem()

    tk.update_idletasks()
    tk.update
    time.sleep(0.25)




















    
