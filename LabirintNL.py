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

    def __str__(self):
        return "Point:X={},Y={}".format(self.x,self.y)
        
    def p_equals(self,p):
        return ((self.x-p.x)+(self.y-p.y))==0


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
    rays=[]
    door={}
    def __init__(self,x,y,scale,color,canvas):
        self.x=x
        self.y=y
        self.scale=scale
        self.step=6
        self.a_step=0.05
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
        self.oval=self.canvas.create_oval(self.x,self.y,self.x+self.scale,self.y+self.scale,fill=self.color)
        self.A=True
        self.B=True
        
    def disFromPointToLine(self,x,y,line):
        vx=1
        vy=1
        if line.ay!=0:
            vy=-line.ax/line.ay
        else:
            vx=-line.ay/line.ax
        print("{} {}".format(vx,vy))
        px,py=line.getIntersectionPoint(vx,vy,x,y)
        if line.isInSector(px,py):
            dis=line.getDist(x,y,px,py)
            print("Dist {}".format(dis))
            return dis
        return 0
        
    def wallContact(self,x,y,walls):
        #print("wallContact")
        for item in walls:
            dis=self.disFromPointToLine(x,y,item)
            if (self.scale/2+5)>dis:
                #self.base_points_arr.append(Point(x,y))
                return False
        return True
    
    def interPointDis(self,p1,p2):
        return math.sqrt(math.pow((p2.x-p1.x),2)+math.pow((p2.y-p1.y),2))

    def getAng(self,p1,p2):
        ax=p2.x-p1.x
        ay=p2.y-p1.y
        r=math.sqrt(ax*ax+ay*ay)
        a=math.acos(ax/r)
        if ay<0:
            a=math.pi*2-a
        return a



    def irradiate(self,room):
        
        for i in range(0,len(room.walls)-1,1):
            if room.walls[i].p2.p_equals(room.walls[i+1].p1):
                pass
            else:
                p=Point(self.canvas.coords(self.oval)[0]+self.scale/2,
                                    self.canvas.coords(self.oval)[1]+self.scale/2)
                a1=self.getAng(p,room.walls[i+1].p1)
                r1=self.interPointDis(p,room.walls[i+1].p1)
                a2=self.getAng(p,room.walls[i].p2)
                r2=self.interPointDis(p,room.walls[i].p2)
                
                cursePoint=Point((room.walls[i+1].p1.x+room.walls[i].p2.x)/2,(room.walls[i+1].p1.y+room.walls[i].p2.y)/2)
                self.door["curse"]=cursePoint
                r=self.interPointDis(room.walls[i+1].p1,room.walls[i].p2)
                print("R={}".format(r))
                rr=self.interPointDis(cursePoint,p)
                if r1>r2:
                    doorSize=self.disFromPointToLine(room.walls[i].p2.x,room.walls[i].p2.y,Line(p,room.walls[i+1].p1))
                    self.door["close"]=room.walls[i].p2
                    self.door["far"]=room.walls[i+1].p1
                    if doorSize<self.scale:
                        self.door["sx"]=(room.walls[i+1].p1.x-room.walls[i].p2.x)/r*self.step
                        self.door["sy"]=(room.walls[i+1].p1.y-room.walls[i].p2.y)/r*self.step
                        return True
                    else:
                        self.door["sx"]=(cursePoint.x-p.x)/rr*self.step
                        self.door["sy"]=(cursePoint.y-p.y)/rr*self.step
                        return False
                else:
                    doorSize=self.disFromPointToLine(room.walls[i+1].p1.x,room.walls[i+1].p1.y,Line(p,room.walls[i].p2))
                    self.door["close"]=room.walls[i+1].p1
                    self.door["far"]=room.walls[i].p2
                    if doorSize<self.scale:
                        self.door["sx"]=(room.walls[i].p2.x-room.walls[i+1].p1.x)/r*self.step
                        self.door["sy"]=(room.walls[i].p2.y-room.walls[i+1].p1.y)/r*self.step
                        return True
                    else:
                        self.door["sx"]=(cursePoint.x-p.x)/rr*self.step
                        self.door["sy"]=(cursePoint.y-p.y)/rr*self.step
                        return False



    def doorSizeCheck(self):
        p=Point(self.canvas.coords(self.oval)[0]+self.scale/2,
                                    self.canvas.coords(self.oval)[1]+self.scale/2)
        doorSize=self.disFromPointToLine(self.door["close"].x,self.door["close"].y,Line(p,self.door["far"]))
        if doorSize>self.scale:
            rr=self.interPointDis(self.door["curse"],p)
            self.door("sx",(self.door["curse"].x-p.x)/rr)
            self.door("sy",(self.door["curse"].y-p.y)/rr)
            return False
        return True     
         
    def moveToDoor(self,room):
        if self.A:
            self.B=self.irradiate(room)
            self.A=False
        self.canvas.move(self.oval,self.door["sx"],self.door["sy"])
        if self.B:
            self.B=self.doorSizeCheck()


    def upAndDown(self,room):
        
        if self.flagStart:
            if self.canvas.coords(self.oval)[0]>room.contur[3].p1.x+5:
                x=-1
                y=0
            else:
                #self.base_points_arr.append(Point(self.x+self.scale/2,self.y+self.scale/2))
                x=0
                y=0
                self.flagStart=False
        else:
            if (self.canvas.coords(self.oval)[0]+self.scale)<room.contur[1].p1.x:
                if (self.canvas.coords(self.oval)[1]<room.contur[0].p1.y)|(self.canvas.coords(self.oval)[1]>room.contur[2].p1.y):
                    print("DONE!")
                    x=0
                    y=0
                    canvas.create_text(room.width/2,room.height/2,text="DONE!")
                #print("Big IF")
                if self.flagY:
                    print("Big IF")
                    if self.wallContact(self.canvas.coords(self.oval)[0]+self.scale/2,
                                        self.canvas.coords(self.oval)[1]+self.scale/2,room.walls):
                        x=self.y_sx
                        y=self.y_sy
                        #self.traces.append(Mark(self.x+self.scale/2,self.y+self.scale/2,"grey",self.canvas))
                    else:
                        self.flagY=False
                        x=self.y_sx
                        y=-self.y_sy
                else:
                    if self.wallContact(self.canvas.coords(self.oval)[0]+self.scale/2,
                                        self.canvas.coords(self.oval)[1]+self.scale/2,room.walls):
                        x=self.y_sx
                        y=-self.y_sy
                        #self.traces.append(Mark(self.x+self.scale/2,self.y+self.scale/2,"grey",self.canvas))
                    else:
                        self.flagY=True
                        x=self.y_sx
                        y=self.y_sy
            
                
        return x,y

        
    def move(self):
        self.x+=1
        self.y=0

    def draw(self,x,y):
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
        
        self.canvas.move(self.oval,x,y)

    
class Line:
    def __init__(self,p1,p2):
        self.p1=p1
        self.p2=p2
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


class DrawableLine(Line):
    def __init__(self,p1,p2,w,color,canvas):
        super().__init__(p1,p2)
        self.width=w
        self.color=color
        self.canvas=canvas
        self.line=self.canvas.create_line(self.p1.x,self.p1.y,self.p2.x,self.p2.y,fill=self.color,width=self.width)

        
    def draw(self):
        self.canvas.move(self.line,0,0)


class Room:
    pre_walls=[]
    walls=[]
    contur=[]
    def __init__(self,x,y,w,h,canvas,color):
        self.x=x
        self.y=y
        self.width=w
        self.height=h
        self.color=color
        self.canvas=canvas
        self.line_w=3
        
        
        self.contur.append(Line(Point(x,y),Point(x+w,y)))#up
        self.contur.append(Line(Point(x+w,y),Point(x+w,y+h)))#right
        self.contur.append(Line(Point(x+w,y+h),Point(x,y+h)))#down
        self.contur.append(Line(Point(x,y+h),Point(x,y)))#left
        
        #self.walls.append(DrawableLine(Point(x,y),Point(x+w/2,y),self.line_w,self.color,canvas))#up
        #self.walls.append(DrawableLine(Point(x+w/2+50,y),Point(x+w,y),self.line_w,self.color,canvas))#up
        #self.walls.append(DrawableLine(Point(x+w,y),Point(x+w,y+h),self.line_w,self.color,canvas))
        #self.walls.append(DrawableLine(Point(x+w,y+h),Point(x,y+h),self.line_w,self.color,canvas))#down
        #self.walls.append(DrawableLine(Point(x,y+h),Point(x,y),self.line_w,self.color,canvas))
        
        self.getRandRoom(2,50)

    def pre_wallsPrint(self):
        for dic in self.pre_walls:
            print("First:{}".format(dic["first"]))
            print("Last:{}".format(dic["last"]))
            for item in dic["doors"]:
                print("P0:{}".format(item[0]))
                print("P1:{}".format(item[1]))

    def overlapControl(self,pos,num,width):
        for door in self.pre_walls[num]["doors"]:
            if door[0].x==self.pre_walls[num]["first"].x:
                if (((pos-width/2)<door[1].y)&((pos+width/2)>door[1].y))|(((pos-width/2)<door[0].y)&((pos+width/2)>door[0].y)):
                    return True
            else:
                if (((pos-width/2)<door[1].x)&((pos+width/2)>door[1].x))|(((pos-width/2)<door[0].x)&((pos+width/2)>door[0].x)):
                    return True
        return False

    def getNewDoor(self,num,width):
        print("get new door {} {}".format(num,width))
        ax=self.contur[num].p2.x-self.contur[num].p1.x
        ay=self.contur[num].p2.y-self.contur[num].p1.y
        r=math.sqrt(ax*ax+ay*ay)
        sx=ax/r
        sy=ay/r
        arr=[]
        
        pos=random.randint(0,r-2*width)
        while self.overlapControl(pos,num,width):
            pos=random.randint(0,r-2*width)
            
        arr.append(Point(self.contur[num].p1.x+sx*(pos-width/2),self.contur[num].p1.y+sy*(pos-width/2)))
        arr.append(Point(self.contur[num].p1.x+sx*(pos+width/2),self.contur[num].p1.y+sy*(pos+width/2)))
        
        self.pre_walls[num]["doors"].append(arr)
        if len(self.pre_walls[num]["doors"])>1:
            self.doorsSort(num)

        
    def interPointDis(self,p1,p2):
        return math.sqrt(math.pow((p2.x-p1.x),2)+math.pow((p2.y-p1.y),2))
    
    def doorsSort(self,index):
        for i in range(0,len(self.pre_walls[index]["doors"])-1,1):
            if self.interPointDis(self.pre_walls[index]["doors"][i][0],
                                  self.pre_walls[index]["first"])>self.interPointDis(self.pre_walls[index]["doors"][i+1][0],
                                                                                     self.pre_walls[index]["first"]):
                temp=self.pre_walls[index]["doors"][i]
                self.pre_walls[index]["doors"][i]=self.pre_walls[index]["doors"][i+1]
                self.pre_walls[index]["doors"][i+1]=temp
                self.doorsSort(index)

    def fromConturToWall(self):
        for i in range(0,len(self.contur),1):
            temp={}
            arr=[]
            temp["first"]=self.contur[i].p1
            temp["last"]=self.contur[i].p2
            temp["doors"]=arr
            self.pre_walls.append(temp)

    def getRandRoom(self,cntDoors,width):
        self.fromConturToWall()
        self.pre_wallsPrint()
        
        for i in range(0,cntDoors,1):
            self.getNewDoor(random.randint(0,3),width)
        self.pre_wallsPrint()   
        for i in range(0,len(self.pre_walls),1):
            if len(self.pre_walls[i]["doors"])>0:
                self.walls.append(DrawableLine(self.pre_walls[i]["first"],self.pre_walls[i]["doors"][0][0],self.line_w,self.color,self.canvas))
                if len(self.pre_walls[i]["doors"])>1:
                    for j in range(0,len(self.pre_walls[i]["doors"])-2,1):
                        self.walls.append(DrawableLine(self.pre_walls[i]["doors"][j][1],self.pre_walls[i]["doors"][j+1][0],self.line_w,self.color,self.canvas))
                self.walls.append(DrawableLine(self.pre_walls[i]["doors"][len(self.pre_walls[i]["doors"])-1][1],
                                               self.pre_walls[i]["last"],self.line_w,self.color,self.canvas))
            else:
                self.walls.append(DrawableLine(self.pre_walls[i]["first"],self.pre_walls[i]["last"],self.line_w,self.color,self.canvas))
        

    def draw(self):
        for item in self.walls:
            item.draw()

background=canvas.create_rectangle(0,0,m_width,m_height,fill="orange")            
room=Room(50,50,500,500,canvas,"brown")
obj=Object(100,200,20,"red",canvas)


def main(): 
    ##obj.draw(*obj.upAndDown(room))
    obj.moveToDoor(room)
    canvas.after(100,main)

canvas.after(100,main)

print('out of cicle')













    
