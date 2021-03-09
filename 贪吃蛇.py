from tkinter import *
import random
import time
root=Tk()
root.resizable(0,0)
root.title('贪吃蛇')
c=Canvas(root,width=300,height=300,bg='white')
v=0.1   #速度
score=0 #分数
text=StringVar()
class body:
    def __init__(self,x,y):
        self.x,self.y=x,y
        self.item=c.create_oval(self.x,self.y,self.x+10,self.y+10,fill='black')
class sneak:
    face=0
    def __init__(self):
        self.bodys=[body(140,230),body(140,240),body(140,250)]
        self.hx,self.hy=140,230
        self.fx,self.fy=140,220
        self.food=body(random.randint(0,29)*10,random.randint(0,29)*10)
    def move(self):
        self.bodys.insert(0,body(self.fx,self.fy))
        self.hx,self.hy=self.bodys[0].x,self.bodys[0].y
        if self.face==0:
            self.fx,self.fy=self.hx,self.hy-10
        elif self.face==1:
            self.fx,self.fy=self.hx+10,self.hy
        elif self.face==2:
            self.fx,self.fy=self.hx,self.hy+10
        elif self.face==3:
            self.fx,self.fy=self.hx-10,self.hy
        if self.hx not in range(0,300) or self.hy not in range(0,300):  #判断是否在场地范围内
            return 0
        for i in self.bodys[1:]:
            if self.hx==i.x and self.hy==i.y:   #判断是否撞到自己
                return 0
        if self.hx==self.food.x and self.hy==self.food.y: #判断是否吃到了食物
            c.delete(self.food.item)
            self.food=body(random.randint(0,29)*10,random.randint(0,29)*10)
            global score
            score+=1
            text.set('score:%d'%score)
        else:
            c.delete(self.bodys.pop().item) #没有吃到食物就删除最后一个body
        c.update()
        time.sleep(v)
        return 1
    def dead(self):
        c.delete(self.food.item)
        while len(self.bodys):
            c.delete(self.bodys.pop().item)
def get(event): #根据按键更改朝向，不允许掉头
    if event.keysym=='Up' and s.face!=2:
        s.face=0
        s.fx,s.fy=s.hx,s.hy-10
    if event.keysym=='Right' and s.face!=3:
        s.face=1
        s.fx,s.fy=s.hx+10,s.hy
    if event.keysym=='Down' and s.face!=0:
        s.face=2
        s.fx,s.fy=s.hx,s.hy+10
    if event.keysym=='Left' and s.face!=1:
        s.face=3
        s.fx,s.fy=s.hx-10,s.hy
def gameover():
    global s,score,top
    top=Toplevel()
    top.title('gameover')
    top.geometry('200x100')
    Label(top,text='游戏结束，你的分数为%d。\n点击下面的按钮重新开始游戏。\n'%score).pack()
    Button(top,text='重新开始',command=restart).pack()
def restart():
    global s,score,top
    top.destroy()
    score=0
    s.dead()
    s=sneak()
    startgame()
s=sneak()
c.pack()
Label(root,textvariable=text).pack(anchor='w')
root.bind('<Key>',get)
def startgame():
    text.set('score: %d'%score)
    while s.move():
        pass
    gameover()
startgame()
root.mainloop()
