from tkinter import *
import random
import time
import gc
root=Tk()
root.title('扫雷')
root.resizable(0,0)
num,xs,ys,size=10,9,9,30 #雷的数量、xy方向的格数、每格的大小
b=[]  #存储block
lei=[]  #存储雷的坐标
nt=StringVar()  #用于显示剩余雷数
tt=StringVar()  #用于显示秒数
game=1  #游戏进行标记，0，1，2分别表示失败，进行，胜利
gamemode=0  #记录模式，0~3分别为简单、中等、困难、自定义
class block:
    pressed=0
    def __init__(self,x,y):
        self.x,self.y=x,y
        self.bt=StringVar() #按键上的字符
        self.t=StringVar()  #按键下的字符
        self.t.set('')
        self.value=0
        self.label=Label(root,textvariable=self.t)
        self.button=Button(root,textvariable=self.bt,command=self.press)
        self.label.place(width=size,height=size,x=self.x*size,y=(self.y+1)*size)
        self.button.place(width=size,height=size,x=self.x*size,y=(self.y+1)*size)
        self.button.bind('<Button-3>',self.sf)
        self.label.bind('<Button-1>',self.b1)
        self.label.bind('<Button-3>',self.b3)
    def press(self):
        if self.bt.get()=='&' or game!=1:
            return
        if self.t.get()=='*':
            gameover()
        self.pressed=1
        self.button.place_forget()
        if self.t.get()=='':    #连锁空格
            for i in [-1,0,1]:
                for j in [-1,0,1]:
                    if self.x+j in range(xs) and self.y+i in range(ys) and b[self.y+i][self.x+j].pressed==0:
                        b[self.y+i][self.x+j].press()
        for i in b:
            for j in i:
                if j.pressed==0 and j.t.get()!='*':  #如果所有不是雷的方块都被按下，胜利
                    return
        win()
    def sf(self,event):
        c=['','&','?']
        if self.bt.get()=='&':
            nt.set(int(nt.get())+1)
        self.bt.set(c[(c.index(self.bt.get())+1)%3])    #右键时循环显示
        if self.bt.get()=='&':
            nt.set(int(nt.get())-1)
    def b1(self,event):
        f=0 #周围的标记个数
        for i in [-1,0,1]:
            for j in [-1,0,1]:
                if self.x+j not in range(xs) or self.y+i not in range(ys):
                    continue
                if b[self.y+i][self.x+j].bt.get()=='&':
                    f+=1
        if f==self.value:
            for i in [-1,0,1]:
                for j in [-1,0,1]:
                    if self.x+j not in range(xs) or self.y+i not in range(ys):
                        continue
                    if b[self.y+i][self.x+j].pressed==1:
                        continue
                    b[self.y+i][self.x+j].press()
    def b3(self,event):
        p=0 #周围没有按下的按键个数
        for i in [-1,0,1]:
            for j in [-1,0,1]:
                if self.x+j not in range(xs) or self.y+i not in range(ys):
                    continue
                if b[self.y+i][self.x+j].pressed==0:
                    p+=1
        if p==self.value:
            for i in [-1,0,1]:
                for j in [-1,0,1]:
                    if self.x+j not in range(xs) or self.y+i not in range(ys):
                        continue
                    if b[self.y+i][self.x+j].pressed==1:
                        continue
                    if b[self.y+i][self.x+j].bt.get()=='&':
                        continue
                    while b[self.y+i][self.x+j].bt.get()!='&':
                        b[self.y+i][self.x+j].sf(event)
class namelist:
    def __init__(self):
        self.top=Toplevel()
        self.top.title('you win')
        self.input=Entry(self.top)
        self.button=Button(self.top,text='确定',command=self.ok)
        self.qbutton=Button(self.top,text='确定',command=self.top.destroy)
        self.t=int(tt.get().split(':')[0])*60+int(tt.get().split(':')[1])   #自己的时间
        if gamemode==3:
            self.show=Label(self.top,text='恭喜，你赢了！')
            self.show.pack()
            self.qbutton.pack()
        else:
            try:
                with open('namelist%d.txt'%gamemode,mode='r') as f:
                    self.text=f.readlines()
                    max=self.text[-1].split()[0]
                    self.maxs=int(max.split(':')[0])*60+int(max.split(':')[1])
                    if self.t>self.maxs and len(self.text)>=5:
                        self.show=Label(self.top,text='恭喜，你赢了！')
                        self.show.pack()
                        self.qbutton.pack()
                    else:
                        self.show=Label(self.top,text='恭喜,新纪录！\n留下你的名字吧：')
                        self.show.pack()
                        self.input.pack()
                        self.button.pack()
            except:
                self.text=[]
                self.show=Label(self.top,text='恭喜,新纪录！\n留下你的名字吧：')
                self.show.pack()
                self.input.pack()
                self.button.pack()
    def ok(self):
        if self.text==[] or self.t>self.maxs:
            self.text.append('%s\t%s\n'%(tt.get(),self.input.get()))
        else:
            try:
                for i in range(len(self.text)):
                    time=self.text[i].split()[0]
                    m=int(time.split(':')[0])*60+int(time.split(':')[1])
                    if self.t<=m:
                        self.text.insert(i,'%s\t%s\n'%(tt.get(),self.input.get()))
                        break
            except:
                self.text.clear()
                self.text.append('%s\t%s\n'%(tt.get(),self.input.get()))
        if len(self.text)>5:
            self.text.pop()
        with open('namelist%d.txt'%gamemode,mode='w') as f:
            f.write(''.join(self.text))
        self.top.destroy()
        menu.showlist()
def start():
    global b,lei,game
    game=1
    root.geometry('%dx%d'%(size*xs,size*(ys+1)))    #调整窗口大小和按钮位置
    show_num.place_forget()
    show_time.place_forget()
    show_restart.place_forget()
    show_num.place(width=size*(xs-1)/2,height=size,x=0,y=0)
    show_time.place(width=size*(xs-1)/2,height=size,x=size*(xs+1)/2,y=0)
    show_restart.place(width=size,height=size,x=size*(xs-1)/2,y=0)
    nt.set(num)
    for i in b: #删除旧方块
        for j in i:
            j.button.place_forget()
            j.label.place_forget()
            del j
    b.clear()
    gc.collect()    #清除内存
    for i in range(0,ys):   #生成新方块
        rb=[]
        for j in range(0,xs):
            new=block(j,i)
            rb.append(new)
        b.append(rb)
    lei=[]
    while len(lei)<num:    #生成雷
        x,y=random.randint(0,xs-1),random.randint(0,ys-1)
        if [x,y] not in lei:
            lei.append([x,y])
            b[y][x].t.set('*')
    print(lei)
    for l in lei:
        x,y=l[0],l[1]
        for i in [-1,0,1]:
            for j in [-1,0,1]:
                if y+i not in range(ys) or x+j not in range(xs):
                    continue
                if b[y+i][x+j].t.get()=='*':
                    continue
                b[y+i][x+j].value+=1
    for i in b: #设置数字
        for j in i:
            if j.value!=0:
                j.t.set('%d'%j.value)
    stime=time.time()
    while game==1:
        t=int(time.time()-stime)
        m,s=t//60,t%60
        tt.set('%d:%d'%(m,s))
        root.update()
def gameover():
    global game
    game=0
    for l in lei:
        x,y=l[0],l[1]
        if b[y][x].bt.get()=='&':
            continue
        b[y][x].pressed=1
        b[y][x].button.place_forget()
def win():
    global game
    if game==2: #防止生成多个窗口
        return
    game=2
    namelist()
class gamemenu:
    def __init__(self):
        self.m=Menu(root)
        self.m1=Menu(self.m,tearoff=0)
        self.m2=Menu(self.m,tearoff=0)
        self.m.add_cascade(label='难度',menu=self.m1)
        self.m.add_cascade(label='查看',menu=self.m2)
        self.m1.add_command(label='简单',command=lambda:self.difficulty(9,9,10,0))
        self.m1.add_command(label='中等',command=lambda:self.difficulty(16,16,40,1))
        self.m1.add_command(label='困难',command=lambda:self.difficulty(30,16,99,2))
        self.m1.add_command(label='自定义',command=self.custom)
        self.m2.add_command(label='排行榜',command=self.showlist)
        root.config(menu=self.m)
    def showlist(self):
        try:
            with open('namelist%d.txt'%gamemode,mode='r') as f:
               t=f.readlines()
        except FileNotFoundError:
            if gamemode==3:
                t='自定义模式不支持排行榜'
            else:
                t='暂无排行榜信息'
        top=Toplevel()
        top.title('排行榜')
        Label(top,text=''.join(t),justify='left').pack()
        Button(top,text='确定',command=top.destroy).pack()
    def difficulty(self,x,y,l,m):
        global xs,ys,num,gamemode,size
        xs,ys,num,gamemode=x,y,l,m
        if ys>25:
            size=20
        elif ys>15:
            size=25
        else:
            size=30
        start()
    def custom(self):
        self.top=Toplevel()
        self.top.title('自定义')
        self.top.resizable(0,0)
        Label(self.top,text='宽度').grid(row=0,column=0)
        Label(self.top,text='高度').grid(row=1,column=0)
        Label(self.top,text='雷数').grid(row=2,column=0)
        sx=Scale(self.top,length=200,from_=3,to=30,orient=HORIZONTAL)
        sy=Scale(self.top,length=200,from_=3,to=30,orient=HORIZONTAL)
        sl=Scale(self.top,length=200,from_=1,to=200,orient=HORIZONTAL)
        sx.grid(row=0,column=1)
        sy.grid(row=1,column=1)
        sl.grid(row=2,column=1)
        Button(self.top,text='取消',command=self.top.destroy).grid(row=0,column=2)
        Button(self.top,text='完成',command=lambda:self.ok(sx.get(),sy.get(),sl.get())).grid(row=2,column=2)
    def ok(self,x,y,l):
        if x*y<=l:
            error=Toplevel()
            Label(error,text='雷数必须小于格数').pack()
            Button(error,text='确定',command=error.destroy).pack()
        else:
            self.top.destroy()
            self.difficulty(x,y,l,3)
show_num=Label(root,textvariable=nt)
show_time=Label(root,textvariable=tt)
show_restart=Button(root,text='O',command=start)
menu=gamemenu()
start()
root.mainloop()