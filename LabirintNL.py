import time
import random
import math
import keyboard
from tkinter import *

m_width=600
m_height=600

tk=Tk()
tk.title("Room")
tk.resizable(0,0)
tk.geometry("600x600+700+100")
canvas=Canvas(tk,width=m_width,height=m_height,bd=0,highlightthickness=0)
canvas.pack()

tk.attributes("-topmost",True)
tk.update()


class Point:
    x=0
    y=0
    def __init__(self,x,y):
        self.x=x
        self.y=y


class Mark():
    arr=[]
    def __init__(self,x,y,color,canvas):
        self.x=x
        self.y=y
        self.color=color
        self.canvas=canvas
        self.r=3
        
    def draw(self):
        self.canvas.create_oval(self.x-self.r/2,self.y-self.r/2,self.x+self.r,self.y+self.r,fill=self.color)


class Object:
    traces=[]
    base_points_arr=[]
    def __init__(self,x,y,scale,color,canvas):
        self.x=x
        self.y=y
        self.scale=scale
        self.step=6
        self.a_step=0.025
        self.color=color
        self.canvas=canvas
        self.R=1000
        self.counter=1
        self.flagY=True
        self.flagX=True
        self.lock=True
        self.flagStart=True
        self.base_points_arr.append(Point(x+scale/2,y+scale/2))
        self.y_sx=math.cos(math.pi/2-self.a_step)*self.step
        self.y_sy=math.sin(math.pi/2-self.a_step)*self.step
        self.x_sx=math.cos(math.pi+self.a_step)*self.step
        self.x_sy=math.sin(math.pi+self.a_step)*self.step
        print("{} {}".format(self.y_sx,self.y_sy))
        
    def wallContact(self,x,y,walls):
        #print("wallContact")
        for item in walls:
            vx=1
            vy=1
            if item.ay!=0:
                vy=-item.ax/item.ay
            else:
                vx=-item.ay/item.ax
            print("{} {}".format(vx,vy))
            px,py=item.getIntersectionPoint(vx,vy,x,y)
            if item.isInSector(px,py):
                dis=item.getDist(x,y,px,py)
                print("Dist {}".format(dis))
                if (self.scale/2+5)>dis:
                    #self.base_points_arr.append(Point(x,y))
                    return False
        return True


    def upAndDown(self,room):
        
        if self.flagStart:
            if self.x>room.contur[3].p1.x+5:
                self.x-=1
            else:
                #self.base_points_arr.append(Point(self.x+self.scale/2,self.y+self.scale/2))
                
                self.flagStart=False
        else:
            if (self.x+self.scale)<room.contur[1].p1.x:
                if (self.y<room.contur[0].p1.y)|(self.y>room.contur[2].p1.y):
                    print("DONE!")
                    canvas.create_text(room.width/2,room.height/2,text="DONE!")
                #print("Big IF")
                if self.flagY:
                    print("Big IF")
                    if self.wallContact(self.x+self.scale/2,self.y+self.scale/2,room.walls):
                        self.x+=self.y_sx
                        self.y+=self.y_sy
                        #self.traces.append(Mark(self.x+self.scale/2,self.y+self.scale/2,"grey",self.canvas))
                    else:
                        self.flagY=False
                        self.x+=self.y_sx
                        self.y-=self.y_sy
                else:
                    if self.wallContact(self.x+self.scale/2,self.y+self.scale/2,room.walls):
                        self.x+=self.y_sx
                        self.y-=self.y_sy
                        #self.traces.append(Mark(self.x+self.scale/2,self.y+self.scale/2,"grey",self.canvas))
                    else:
                        self.flagY=True
                        self.x+=self.y_sx
                        self.y+=self.y_sy
     

    
    def move(self,dx,dy):
        self.x=dx
        self.y=dy

    def draw(self):
##        for item in self.traces:
##            item.draw()
        
##        if len(self.base_points_arr)>2:
##            print(len(self.base_points_arr))
##            for i in range(0,len(self.base_points_arr)-1,1):
##                self.canvas.create_line(self.base_points_arr[i].x,
##                                        self.base_points_arr[i].y,
##                                        self.base_points_arr[i+1].x,
##                                        self.base_points_arr[i+1].y,
##                                        fill=self.color,width=2)
##        self.canvas.create_line(self.base_points_arr[len(self.base_points_arr)-1].x,
##                                self.base_points_arr[len(self.base_points_arr)-1].y,
##                                self.x+self.scale/2,
##                                self.y+self.scale/2,
##                                fill=self.color,width=2)
        self.canvas.create_oval(self.x,self.y,self.x+self.scale,self.y+self.scale,fill=self.color)
        

    
class Line:
    def __init__(self,p1,p2,w,color,canvas):
        self.p1=p1
        self.p2=p2
        self.width=w
        self.color=color
        self.canvas=canvas
        self.ax=p2.x-p1.x
        self.ay=p2.y-p1.y
        
    def set(self,v,p):
        self.p1=p
        self.ax=v.x
        self.ay=v.y
        

    def getDist(self,p1,p2):
        return math.sqrt(math.pow((p1.x-p2.x),2)+math.pow((p1.y-p2.y),2))

    def getDist(self,x1,y1,x2,y2):
        return math.sqrt(math.pow((x2-x1),2)+math.pow((y2-y1),2))
       
    def isInSector(self,p):      
        if self.p1.x>self.p2.x:
            max_x=self.p1.x
            min_x=self.p2.x
        else:
            min_x=self.p1.x
            max_x=self.p2.x
        if self.p1.y>self.p2.y:
            max_y=self.p1.y
            min_y=self.p2.y
        else:
            min_y=self.p1.y
            max_y=self.p2.y
        return (p.x>=min_x)&(p.x<=max_x)&(p.y>=min_y)&(p.y<=max_y)

    def isInSector(self,x,y):      
        if self.p1.x>self.p2.x:
            max_x=self.p1.x
            min_x=self.p2.x
        else:
            min_x=self.p1.x
            max_x=self.p2.x
        if self.p1.y>self.p2.y:
            max_y=self.p1.y
            min_y=self.p2.y
        else:
            min_y=self.p1.y
            max_y=self.p2.y
        return (x>=min_x)&(x<=max_x)&(y>=min_y)&(y<=max_y)
        
    def getIntersectionPoint(self,l):
        
        if self.ax!=0:
            a=l.ax*self.ay*self.p1.x
            b=l.ax*self.ax*self.p1.y
            c=l.ax*self.ax*l.p1.y
            d=l.ay*self.ax*l.p1.x
            e=l.ax*self.ay-l.ay*self.ax
            x=(a-b+c-d)/e
            y=(self.ay*(x-self.p1.x)+self.ax*self.p1.y)/self.ax
        else:
            a=l.ay*self.ay*self.p1.x
            b=l.ay*self.ax*self.p1.y
            c=l.ay*self.ay*l.p1.x
            d=l.ax*self.ay*l.p1.y
            e=l.ax*self.ay-l.ay*self.ax
            y=(a-b-c+d)/e
            x=(self.ax*(y-self.p1.y)+self.ay*self.p1.x)/self.ay
            
        return Point(x,y)

    def getIntersectionPoint(self,bx,by,x,y):
        
        if self.ax!=0:
            a=bx*self.ay*self.p1.x
            b=bx*self.ax*self.p1.y
            c=bx*self.ax*y
            d=by*self.ax*x
            e=bx*self.ay-by*self.ax
            rx=(a-b+c-d)/e
            ry=(self.ay*(rx-self.p1.x)+self.ax*self.p1.y)/self.ax
        else:
            a=by*self.ay*self.p1.x
            b=by*self.ax*self.p1.y
            c=by*self.ay*x
            d=bx*self.ay*y
            e=bx*self.ay-by*self.ax
            ry=(a-b-c+d)/e
            rx=(self.ax*(ry-self.p1.y)+self.ay*self.p1.x)/self.ay
            
        return rx,ry
        
    def draw(self):
        self.canvas.create_line(self.p1.x,self.p1.y,self.p2.x,self.p2.y,fill=self.color,width=self.width)


class Room:
    walls=[]
    contur=[]
    def __init__(self,x,y,w,h,color,canvas):
        self.x=x
        self.y=y
        self.width=w
        self.height=h
        self.color=color
        self.canvas=canvas
        self.line_w=3
        
        self.contur.append(Line(Point(x,y),Point(x+w,y),self.line_w,color,canvas))#up
        self.contur.append(Line(Point(x+w,y),Point(x+w,y+h),self.line_w,color,canvas))#right
        self.contur.append(Line(Point(x+w,y+h),Point(x,y+h),self.line_w,color,canvas))#down
        self.contur.append(Line(Point(x,y+h),Point(x,y),self.line_w,color,canvas))#left
        
        self.walls.append(Line(Point(x,y),Point(x+w/2,y),self.line_w,color,canvas))#up
        self.walls.append(Line(Point(x+w/2+50,y),Point(x+w,y),self.line_w,color,canvas))#up
        self.walls.append(Line(Point(x+w,y),Point(x+w,y+h),self.line_w,color,canvas))
        self.walls.append(Line(Point(x+w,y+h),Point(x,y+h),self.line_w,color,canvas))#down
        self.walls.append(Line(Point(x,y+h),Point(x,y),self.line_w,color,canvas))

    def draw(self):
        for item in self.walls:
            item.draw()

room=Room(50,50,500,500,"brown",canvas)
obj=Object(100,200,20,"red",canvas)


while True: 
    
    canvas.create_rectangle(0,0,m_width,m_height,fill="orange")
    canvas.create_text(50,20,text="Press 'q' to exit")
    
    room.draw()
    obj.upAndDown(room)
    obj.draw()

    
    tk.update_idletasks()
    tk.update

    
    
    if keyboard.is_pressed('q'):   # Клавиша для остановки цикла
        break
    
    time.sleep(0.05)


print('out of cicle')













    
