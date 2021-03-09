from tkinter import*
import random
root=Tk()
root.title('2048')
root.resizable(0,0)
root.geometry('400x400')
size=4#边长
def cmplist(a,b):   #二维列表比较函数，完全相同返回0
    for c,d in zip(a,b):
        for e,f in zip(c,d):
            if e!=f:
                return 1
    return 0
class block:
    def __init__(self):
        self.text=StringVar()
        self.label=Label(root,bg='white',relief='solid',borderwidth=1,font='bold',textvariable=self.text)
class blocks:
    def __init__(self):
        self.blist=[]   #存储组件
        self.vlist=[]   #存储数据
        for i in range(size):
            new=[]
            newv=[]
            for j in range(size):
                newb=block()
                newb.label.place(width=100,height=100,x=100*j,y=100*i)
                new.append(newb)
                newv.append(0)
            self.blist.append(new)
            self.vlist.append(newv)
        x,y=random.randint(0,size-1),random.randint(0,size-1)
        self.vlist[y][x]=random.randrange(2,5,2)
        root.bind('<Up>',self.up)
        root.bind('<Down>',self.down)
        root.bind('<Left>',self.left)
        root.bind('<Right>',self.right)
    def show(self):
        for i in range(size):
            for j in range(size):
                if self.vlist[i][j]==0:
                    self.blist[i][j].text.set('')
                else:
                    self.blist[i][j].text.set(self.vlist[i][j])
        root.update()
    def do(self):
        lastlist=[]
        for i in self.vlist:    #备份vlist
            lastlist.append(i.copy())
        for i in self.vlist:
            while i.count(0):   #清除0
                i.remove(0)
            for j in range(len(i)-1):   #合并值相同的项
                if j+1<len(i) and i[j]==i[j+1]:
                    i[j]+=i.pop(j+1)
            while len(i)<size:  #补充0
                i.append(0)
        if cmplist(self.vlist,lastlist):
            for i in self.vlist:
                x,y=random.randint(0,size-1),random.randint(0,size-1)
                while self.vlist[x][y]!=0:
                    x,y=random.randint(0,size-1),random.randint(0,size-1)
                else:
                    self.vlist[x][y]=random.randrange(2,5,2)
                    break
    def up(self,event):
        self.vlist=list(map(list,zip(*self.vlist)))   #将list转置
        self.do()
        self.vlist=list(map(list,zip(*self.vlist)))
        self.show()
    def down(self,event):
        self.vlist.reverse()
        self.vlist=list(map(list,zip(*self.vlist)))
        self.do()
        self.vlist=list(map(list,zip(*self.vlist)))
        self.vlist.reverse()
        self.show()
    def left(self,event):
        self.do()
        self.show()
    def right(self,event):
        for i in self.vlist:
            i.reverse()
        self.do()
        for i in self.vlist:
            i.reverse()
        self.show()
game=blocks()
game.show()
root.mainloop()