print("Hello")

from tkinter import *
import random
import math

m_width=600
m_height=600
background_color="pink"

tk=Tk()#window
tk.title("Room")#its title
tk.resizable(0,0)# cannot resize
tk.geometry("600x600+600+100")#600 на 600 - размер и 600 на 100 - положение
#tk.wm_attributes("-tompost",1)#overlape - не работает!
tk.attributes("-topmost",True)## - работает

canvas=Canvas(tk,width=m_width,height=m_height,bd=0,highlightthickness=0)#окно, его ширина, высота, толщина границ



canvas.pack()
tk.update()


class Point:
    def __init__(self,x,y):
        self.x=x
        self.y=y
        
    def __eq__(self,p):
        return (self.x==p.x)&(self.y==p.y)
    
    def __lt__(self,p):
        return ((self.x==p.x)&(self.y<p.y))|((self.y==p.y)&(self.x<p.x))
    
    def __gt__(self,p):
        return ((self.x==p.x)&(self.y>p.y))|((self.y==p.y)&(self.x>p.x))

    def __str__(self):
        return "{} {}".format(self.x,self.y)


class Line:
    def __init__(self,p1,p2):
        self.p1=p1
        self.p2=p2
        self.ax=p2.x-p1.x
        self.ay=p2.y-p1.y
        self.r=self.dist(p1,p2)
        self.sx=self.ax/self.r
        self.sy=self.ay/self.r
        self.a=self.getAng()

    def __str__(self):
        return "{},{},{}".format(self.p1,self.p2,self.a)

    def getAng(self):
        a=math.acos(self.sx)
        if self.sy<0:
            a=math.pi*2-a
        return a

    def dist(self,p1,p2):
        return math.sqrt(self.ax*self.ax+self.ay*self.ay)

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
        # print("intersection point {},{}".format(rx,ry))            
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



class MyObject:
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

    def getVector(self,x,y,line):
        vx=1
        vy=1
        if line.ay!=0:
            vy=-line.ax/line.ay
        else:
            vx=-line.ay/line.ax
        # print("{} {}".format(vx,vy))
        
        return vx,vy


    def wallContact(self,x,y,walls):
        # print("wallContact")
        for item in walls:
            px,py=item.getIntersectionPoint(*self.getVector(x,y,item),x,y)
            if (item.getDist(x,y,px,py)<self.scale/2)&(item.isInSector(px,py)):
                print("Contact")
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

    def move(self,x,y,walls):
        
        if self.wallContact(self.canvas.coords(self.oval)[0]+self.scale/2+x,
                            self.canvas.coords(self.oval)[1]+self.scale/2+y,walls):
            self.canvas.move(self.oval,x,y)



class Room:
    ref_points=[]
    contur=[]
    walls=[]
    pre_walls=[]
    def __init__(self,x,y,w,h,n,dw,canvas):
        self.x=x
        self.y=y
        self.width=w
        self.height=h
        self.n=n
        self.wall_color="red"
        self.ref_points.append(Point(x,y))
        self.ref_points.append(Point(x+w,y))
        self.ref_points.append(Point(x+w,y+h))
        self.ref_points.append(Point(x,y+h))
        self.door_width=dw
        self.canvas=canvas
        
        self.getContur()
        self.getDoors()
        
        # for i in self.ref_points:
        #     print(i)
        
        # for i in self.contur:
        #     print(i)
        

    def getContur(self):
        for i in range(len(self.ref_points)):
            if i==len(self.ref_points)-1:
                self.contur.append(Line(self.ref_points[i],self.ref_points[0]))
            else:
                self.contur.append(Line(self.ref_points[i],self.ref_points[i+1]))
    
                
    def intersectionControl(self,arr,k2):
        print("Control")

        for i in arr:
            print("{},{}".format(i[0],i[1]))
        
        for k1 in arr:
            print("{},{};{},{}".format(k1[0],k1[1],k2[0],k2[1]))
            
            if (k1[0].x==k1[1].x)&(k2[0].x==k2[1].x):
                if (((k2[0].y>k1[0].y)&(k2[0].y<k1[1].y))|((k1[0].y>k2[0].y)&(k1[0].y<k2[1].y)))|(((k2[1].y>k1[1].y)&(k2[1].y<k1[0].y))|((k1[1].y>k2[1].y)&(k1[1].y<k2[0].y))):
                    print("False")
                    return False
            if (k1[0].y==k1[1].y)&(k2[0].y==k2[1].y):
                if (((k2[0].x>k1[0].x)&(k2[0].x<k1[1].x))|((k1[0].x>k2[0].x)&(k1[0].x<k2[1].x)))|(((k2[1].x>k1[1].x)&(k2[1].x<k1[0].x))|((k1[1].x>k2[1].x)&(k1[1].x<k2[0].x))):
                    print("False")
                    return False
                
        print("True")
        return True
    

    def arrSort(self,arr):
        print("sort")
        
        print("before")
        for p in arr:
            print(p)
        print("=============") 
        
        for i in range(len(arr)):
            for j in range(len(arr)):
                if arr[i]>arr[j]:
                    temp=arr[i]
                    arr[i]=arr[j]
                    arr[j]=temp
        
        print("after")
        for p in arr:
            print(p)
        print("=============")   

    def getDoors(self):
        for i in range(len(self.ref_points)):
            temp={}
            temp["wall"]=[]
            temp["holes"]=[]
            if i==len(self.ref_points)-1:
                temp["wall"].append(self.ref_points[i])
                temp["wall"].append(self.ref_points[0])
            else:
                temp["wall"].append(self.ref_points[i])
                temp["wall"].append(self.ref_points[i+1])
                
            self.pre_walls.append(temp)

        for item in self.pre_walls:
            print("{},{}".format(item["wall"][0],item["wall"][1]))

        ii=0

        while ii <self.n:
            wall=random.randint(0,3)
            l=self.contur[wall]    
            r=random.randint(self.door_width,l.r-3*self.door_width)
            
            p1=Point(l.p1.x+l.sx*r,l.p1.y+l.sy*r)
            p2=Point(l.p1.x+l.sx*(r+self.door_width),l.p1.y+l.sy*(r+self.door_width))
            
            print("While")
            if self.intersectionControl(self.pre_walls[wall]["holes"],(p1,p2)):
                self.pre_walls[wall]["holes"].append((p1,p2))
                ii+=1
                
        for item in self.pre_walls:
            print("wall: ",end=" ")
            print("{},{}".format(item["wall"][0],item["wall"][1]))
            print("holes: ",end=" ")
            for h in item["holes"]:
                print("{},{}".format(h[0],h[1]),end=" ")
            print("\n")
            
        for item in self.pre_walls:
            if len(item["holes"])>0:
                for m in item["holes"]:
                    item["wall"].append(m[0])
                    item["wall"].append(m[1])
                self.arrSort(item["wall"])

        for item in self.pre_walls:
            if len(item["wall"])==2:
                self.walls.append(DrawableLine(item["wall"][0],item["wall"][1],3,"red",self.canvas)) 
            else:
                for w in range(0,len(item["wall"]),2):
                    self.walls.append(DrawableLine(item["wall"][w],item["wall"][w+1],3,"red",self.canvas))        




def function(event):
    step=4
    if event.keysym=="Up":
        print("UP")
        obj.move(0,-step,room.walls)
    elif event.keysym=="Down":
        print("DOWN")
        obj.move(0,step,room.walls)
    elif event.keysym=="Right":
        print("RIGHT")
        obj.move(step,0,room.walls)
    elif event.keysym=="Left":
        print("LEFT")
        obj.move(-step,0,room.walls)

room=Room(30,30,500,500,5,50,canvas)
obj=MyObject(250,100,20,"blue",canvas)

        
canvas.bind_all("<KeyPress-Left>",function)
canvas.bind_all("<KeyPress-Right>",function)
canvas.bind_all("<KeyPress-Up>",function)
canvas.bind_all("<KeyPress-Down>",function)

if __name__ == '__main__':
    tk.mainloop()


##def main(): 
##   
##	
##    canvas.after(100,main)
##
##canvas.after(100,main)

