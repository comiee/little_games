from pygame import *
from pygame.locals import *
import time
init()
display.set_caption('汉诺塔')
w,h=800,600
screen=display.set_mode((w,h))
class game:
    def __init__(self,level=3):
        self.level=level
        self.data=[[],[],[]]
        for i in range(level,0,-1):
            self.data[0].append(i)
        self.hand=None
        self.time=time.time()
        #调用do开始执行
        self.do()
    def show(self):
        xs,ys=15,15 #宽度和厚度
        for i in range(int(w/6),w,int(w/3)):    #显示背景
            draw.rect(screen,(0,0,0),(i-5,int(h/2),5,int(h/2)),0)
        for i,a in enumerate(self.data):    #显示圆盘
            for j,b in enumerate(a):
                x=w/6+i*w/3-b*xs
                y=h-(j+1)*ys
                draw.rect(screen,(0,0,0),(int(x),int(y),2*b*xs,ys),0)
        if self.hand!=None: #显示顶部的一个圆盘
            mi=int(mouse.get_pos()[0]/(w/3))
            mx=w/6+mi*w/3-self.hand*xs
            draw.rect(screen,(0,0,0),(int(mx),int(h/3),2*self.hand*xs,ys),0)
        screen.blit(font.Font(None,60).render("%d"%(time.time()-self.time),True,(0,255,0)),(w/2,h/6))
    def press(self,e):
        b=e.button
        x,y=e.pos
        i=int(x/(w/3))
        if b==1 and self.hand==None:
            if self.data[i]==[]:
                print('\a')
                return
            self.hand=self.data[i].pop()
        elif b==1 and self.hand!=None:
            if self.data[i]!=[] and self.hand>self.data[i][-1]:
                print('\a')
                return
            self.data[i].append(self.hand)
            self.hand=None
        if self.data[0]==[] and self.data[1]==[] and self.hand==None:
            t=time.time()-self.time
            print(t)
            self.win()
    def do(self):
        while 1:
            screen.fill((255,255,255)) #白色背景
            for e in event.get():
                if e.type==QUIT:
                    return
                if e.type==MOUSEBUTTONDOWN:
                    self.press(e)
            self.show()
            display.update()
    def win(self):
        self.show()
        screen.blit(font.Font(None,60).render("YOU WIN",True,(255,0,0)),(270,270))
        display.update()
        while 1:
            for e in event.get():
                if e.type==QUIT:
                    exit(0)
            m=mouse.get_pressed()
            if m[2]:
                break
        self.__init__(self.level+1)
game()