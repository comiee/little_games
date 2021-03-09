from pygame import *
from pygame.locals import *
import time
import random
init()
display.set_caption('flying bird')
w,h=800,600
screen=display.set_mode((w,h))
class bird:
    def __init__(self):
        self.x=int(w/8)
        self.y=int(h/2)
        self.score=0
        self.scoreImage=font.Font(None,60).render("%d"%self.score,True,(0,255,0))
    def show(self):
        draw.circle(screen,(0,0,0),(self.x,self.y),20,0)
        screen.blit(self.scoreImage,(400,50))
    def move(self):
        m=mouse.get_pressed()
        k=key.get_pressed()
        if self.y>0 and (m[0] or k[K_UP]):
            self.y-=3
        else:
            self.y+=3
class pillar:
    def __init__(self):
        self.x=w
        self.y1=random.randint(0,h-150)
        self.y2=self.y1+150
    def show(self):
        draw.rect(screen,(0,0,0),(self.x,0,50,self.y1),0)
        draw.rect(screen,(0,0,0),(self.x,self.y2,50,h-self.y2),0)
    def move(self):
        self.x-=1
class game:
    def __init__(self):
        self.player=bird()
        self.pillars=[pillar(),]
        self.score=0
    def do(self):
        time.sleep(0.01)
        for i in self.pillars:
            i.move()
            i.show()
        self.player.move()
        self.player.show()
        if self.player.y>h: #落地死
            gameover()
        for i in self.pillars:
            if i.x-15<self.player.x<i.x+50+15:
                if self.player.y<i.y1+15 or self.player.y>i.y2-15: #撞墙死
                    gameover()
            if i.x==self.player.x:
                self.player.score+=1
                self.player.scoreImage=font.Font(None,60).render("%d"%self.player.score,True,(0,255,0))
        if self.pillars[-1].x<w-200:
            self.pillars.append(pillar())
        if self.pillars[0].x<-200:
            del self.pillars[0]
def gameover():
    global g
    textImage=font.Font(None,60).render("GAME OVER",True,(255,0,0))
    screen.blit(textImage,(270,270))
    display.update()
    while 1:
        for e in event.get():
            if e.type==QUIT:
                exit(0)
        m=mouse.get_pressed()
        if m[2]:
            break
    del g
    g=game()
g=game()
while 1:
    screen.fill((255,255,255)) #白色背景
    for e in event.get():
        if e.type==QUIT:
            exit(0) #0表示正常退出，不会抛出异常
    g.do()
    display.update()