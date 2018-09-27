
import random
import sys
import numpy as np

import Tkinter as tk
from Tkinter import *
import random

class GUI(tk.Tk):
    def __init__(self, dim,*args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.len = 25
        self.canvas = tk.Canvas(self, width=self.len*dim, height=self.len*dim)
        self.canvas.pack(side="top", fill="both", expand="true")
        self.isopen = True
        

        self.rect = {}
        self.oval = {}
        self.label = {}
        for column in range(dim):
            for row in range(dim):
                x1 = column*self.len
                y1 = row * self.len
                x2 = x1 + self.len
                y2 = y1 + self.len
                self.rect[row,column] = self.canvas.create_rectangle(x1,y1,x2,y2, fill="white", tags="rect")
                self.label[row,column]  = self.canvas.create_text(x1+13, y1+13, fill='#000',text="",tags="label")

    def redraw(self, loc,val):

        if val == -2:
            val = "*"
            self.canvas.itemconfig(self.rect[loc[0],loc[1]],fill="red")
        else:
            self.canvas.itemconfig(self.rect[loc[0],loc[1]],fill="snow4")
        self.canvas.itemconfig(self.label[loc[0],loc[1]],text=str(val))
             
    def onclose(self):
        self.isopen = False
        self.destroy()
        
    def popup(self,loc):
        self.w=popupWindow(self,loc)
        self.wait_window(self.w.top)
    def endpopup(self,s):
        self.end = endWindow(self,s)
        self.wait_window(self.end.top)

    def entryValue(self):
        if hasattr(self.w, 'value'):
            return self.w.value
        else:
            self.destroy()
            return 10
            

class popupWindow(object):
    def __init__(self,master,loc):
        
        top=self.top=Toplevel(master)
        self.l=Label(top,text="Enter value at location:" + str(loc))
        self.l.pack()
        self.e=Entry(top)
        self.e.pack()
        self.b=Button(top,text='Ok',command=self.cleanup)
        self.b.pack()
    
    def cleanup(self):
        self.value=self.e.get()
        self.top.destroy()


class endWindow(object):
    def __init__(self,master,s):
        self.master= master
        top=self.top=Toplevel(master)
        self.l=Label(top,text=s)
        self.l.pack()
        self.b=Button(top,text='Ok',command=self.cleanup)
        self.b.pack()
    
    def cleanup(self):
        self.top.destroy()
        self.master.destroy()
    
    




class Minesweeper():


    def __init__(self,row,columns,mines,mode):

 
        #self.inp = [[0,1,-2,3,2,2,2,-2,2],[1,2,3,-2,-2,2,-2,3,-2],[2,-2,3,2,2,3,2,3,1],[2,-2,2,1,1,2,-2,1,0],[2,2,2,1,-2,3,2,2,0],[1,-2,3,3,2,2,-2,2,1],[1,2,-2,-2,1,1,1,2,-2],[0,1,2,2,1,0,0,1,1],[0,0,0,0,0,0,0,0,0]]    
        self.mode = mode
        self.r = row
        self.c = columns
        self.inp = self.generateBoard(mines)
        self.gameOver = False
        self.bombCells = []
        self.cells = [[9 for i in range(self.c)] for j in range(self.r)]
        self.cellPbty = np.array([[1 for i in range(self.c)] for j in range(self.r)],dtype=np.float)
        self.pbtyLimit = 0.2
        self.exploredCells = []
        self.app  = GUI(self.r)
        self.app.title('Minesweeper')
        self.chainLength = 0

    #generation of random board
        
    def generateBoard(self, mines):
        bombLocs = []
        count = 0
        while(count < mines):
            r = random.randint(0,self.r-1)
            c = random.randint(0,self.c-1)
            if [r,c] not in bombLocs:
                bombLocs.append([r,c])
                count += 1
        board = [[0 for i in range(self.r)] for j in range(self.c)]
        for i in bombLocs:
            board[i[0]][i[1]] = -2
            for j in self.findNeighbors(i):
                if j not in bombLocs:
                    board[j[0]][j[1]] += 1
        #print(board)
        return board
                
        
        

    def displayCells(self):
        print('*****************')
        for i in range(self.r):
            print(self.cells[i][:])

# find all neighbors within the bounds of the board
    def findNeighbors(self,a):
            a =  [[a[0]+1,a[1]],[a[0]+1,a[1]+1],[a[0]+1,a[1]-1],[a[0]-1,a[1]],[a[0]-1,a[1]+1],[a[0]-1,a[1]-1],[a[0],a[1]+1],[a[0],a[1]-1]]
            b = []
            for i in a:
                    if  self.withinBounds(i):
                            b.append(i)
            return b


    def withinBounds(self,x):
            if  x[0]>=0 and x[0]<self.r and x[1]>=0 and x[1]<self.c:
                    return True
            else:
                    return False

            
    def getUserValue(self,a):
        #uncomment this to get input from the user
        if  not self.mode:
            self.app.popup(a)
            val = int(self.app.entryValue())
        else:
            val  =  self.inp[a[0]][a[1]]
        if val == 10:
            sys.exit()
            
        if val == -2:
            self.gameOver = True
            self.app.endpopup('computer lost:' + str(a))
            self.app.isopen = False
        else:
            return val

    def isKnown(self,a):
        if self.cells[a[0]][a[1]] not in [9,-2]:
            return True

 # explores all the neighbors it is used when a cell value is zero           
    def exploreNeighbors(self,a):
        for f in self.findNeighbors(a):
            if not self.isKnown(f):
                self.setCellValue(f,False)


    def outer(self,a):
        r = self.r
        c = self.c
        if (a[0]>=1 and a[0]<r-1 and (a[1] == 0 or a[1] == c-1)) or (a[1]>=1 and a[1]<c-1 and (a[0] == 0 or a[0] == r-1)):
                return 5
        elif (a[0] == 0 and a[1] == 0) or (a[0] == 0 and a[1] == c-1) or (a[0] == c-1 and a[1] == 0) or (a[0] == r-1 and a[0] == c-1):
                return 3
        else:
                return 8
                
    def neighborsKnown(self,y):
        c=0
        b=0
        unknown = []
        for n in self.findNeighbors(y):
            if self.isKnown(n):
                c += 1
            elif n in self.bombCells:
                b += 1
            else:
                unknown.append(n)
        return [unknown,c,b]

    def selectQuery(self):
        a = random.uniform(0,1)
        if a <= 0.005:
            print("random")
            return self.randomQuery()
        else:
            print("query")
            return self.smartQuery()

        
    def randomQuery(self):
        a =  [random.randint(0,self.r-1),random.randint(0,self.c-1)]
        while(self.isKnown(a)):
            a =  [random.randint(0,self.r-1),random.randint(0,self.c-1)]
        return a
        

    def smartQuery(self):
          
          self.updateCellPbty()
          min = np.where(self.cellPbty == np.min(self.cellPbty))
          ind = random.randint(0,(len(min[0])-1))
          x =  [min[0][ind],min[1][ind]]
          if self.cellPbty[x[0]][x[1]] >= self.pbtyLimit:
              min =np.where(self.cellPbty == 1)
              if len(min[0]) == 0:
                  return x
              ind = random.randint(0,(len(min[0])-1))
              return [min[0][ind],min[1][ind]]
          return x

    def  displayCellPbty(self):
        for i in range(self.r):
            print(self.cellPbty[i][:])
                
                
    def updateCellPbty(self):
        for i in range(self.r):
            for j in range(self.c):
                a= [i,j]
                d = self.neighborsKnown([i,j])
                if self.cells[i][j] == -2 or self.cells[i][j] == 0 or len(d[0])==0:
                    self.cellPbty[i][j] = 2
                elif self.isKnown([i,j]):
                    self.cellPbty[i][j] = 2
                    pbty = (self.cells[i][j] - d[2])/float(len(d[0]))
                    for k in d[0]:
                        if self.cellPbty[k[0]][k[1]] != 1:
                            if self.cellPbty[k[0]][k[1]] < pbty:
                                self.cellPbty[k[0]][k[1]] = pbty
                        else:
                            self.cellPbty[k[0]][k[1]] = pbty


    def unlockHelper(self,x):
        n = self.findNeighbors(x)
        for i in n:
            self.unlockCell(i)

    def addToBombCells(self,x):
        if x not in self.bombCells:
            self.bombCells.append(x)

            
    def unlockCell(self,x):
        [i,j] =x
        if self.isKnown([i,j]):
            cellVal = self.cells[i][j]
            d = self.neighborsKnown([i,j])
            o = self.outer([i,j])
            if d[1]+d[2] == o or cellVal == 0:
                pass
            elif cellVal == d[2]:
                for k in d[0]:
                    self.setCellValue(k,False)
                    self.unlockHelper(k)
            elif cellVal == (o-d[1]):
                for l in d[0]:
                    self.addToBombCells(l)
                    self.setCellValue(l,True)
                    
    def setCellValue(self,loc,isBomb):
        if not  isBomb  :
            if not self.isKnown(loc):
                val = self.getUserValue(loc)
                
                self.cells[loc[0]][loc[1]] = val
                
                self.show(loc)
                if val == 0:
                    
                    self.exploreNeighbors(loc)
                    
                    return
        else:
            self.cells[loc[0]][loc[1]] = -2
            self.show(loc)
            return

    def show(self,loc):
        
        if self.app.isopen:
            self.app.redraw(loc,self.cells[loc[0]][loc[1]])
            self.app.update_idletasks()
            self.app.update()
            
            
        
        
                
    def unlockCells(self):
        for i in range(self.r):
            for j in range(self.c):
                #print(i,j)
                if self.isKnown([i,j]):
                    cellVal = self.cells[i][j]
                    d = self.neighborsKnown([i,j])
                    o = self.outer([i,j])
                    if d[1]+d[2] == o or cellVal == 0:
                        pass
                    elif cellVal == d[2]:
                        for k in d[0]:
                            self.setCellValue(k,False)
                            self.unlockHelper(k)
                    elif cellVal == (o-d[1]):
                        for l in d[0]:
                            self.addToBombCells(l)
                            self.setCellValue(l,True)
                            self.unlockHelper([l[0],l[1]])

    def setExploredCells(self):
        self.exploredCells = []
        for i in range(self.r):
            for j in range(self.c):
                if self.isKnown([i,j]):
                    if len(self.neighborsKnown([i,j])[0]) != 0:
                        self.exploredCells.append([i,j])
                        
    
 
        
    def evidenceUnlock(self):
        for k in self.exploredCells:
            for j in self.exploredCells:
                if k != j:
                    a = k
                    b = j
                    c = self.neighborsKnown(a)
                    d = self.neighborsKnown(b)
                    first = [tuple(i) for i in c[0]]
                    second = [tuple(j) for j in d[0]]
                    inter = set(first).intersection(second)
                    if  len(inter) != 0:
                        if len(first) > len(second) and len(set(second) - set(first)) == 0:
                               d1 = set(first) - set(second)
                               d2 = abs(self.cells[b[0]][b[1]] - d[2] - self.cells[a[0]][a[1]] + c[2])
                               if d2 == 0:
                                   for i in list(d1):
                                       self.setCellValue([i[0],i[1]],False)
                               else:
                                   if len(d1) == d2:
                                       for i in list(d1):
                                           self.addToBombCells([i[0],i[1]])
                                           self.setCellValue([i[0],i[1]],True)
                                
                        if len(second) > len(first) and len(set(first) - set(second)) == 0:
                           d1 = set(second) - set(first)
                           d2 = abs(self.cells[a[0]][a[1]] - c[2] - self.cells[b[0]][b[1]] + d[2] )
                           if d2 == 0:
                               for i in list(d1):
                                   self.setCellValue([i[0],i[1]],False)
                           else:
                               if len(d1) == d2:
                                   for i in list(d1):
                                       self.addToBombCells([i[0],i[1]])
                                       self.setCellValue([i[0],i[1]],True)
                                       
                        if len(second) == len(first):
                            g = set(second) - inter
                            h = set(first) - inter
                            if len(g) == 1 and len(h) == 1 :
                                g = list(g)[0]
                                h = list(h)[0]
                                f= self.cells[g[0]][g[1]]
                                s= self.cells[h[0]][h[1]]
                                if abs( s-f ) == 1:
                                    if f>s:
                                        self.addToBombCells([g[0],g[1]])
                                        self.setCellValue([g[0],g[1]],True)
                                        self.setCellValue([h[0],h[1]],False)
                                    else:
                                        self.addToBombCells([h[0],h[1]])
                                        self.setCellValue([h[0],h[1]],True)
                                        self.setCellValue([g[0],g[1]],False)
                                        
                                        
                                        
                                        
                                        
                                    
        
    def change(self):
        count = 0
        for i in range(self.r):
            for j in range(self.c):
                if self.cells[i][j] != 9:
                    count += 1
        return count
                    
        
        
                               
    def isGameOver(self):
        for i in range(self.r):
            if 9 in self.cells[i][:]:
                return False
        print("Computer won!!")
        return True

    def run(self):
        self.app.protocol("WM_DELETE_WINDOW", self.app.onclose)
        while not self.isGameOver() and not self.gameOver:
            x = self.selectQuery()
            self.chainLength = 1
            self.setCellValue(x,False)
            c = self.change()
            self.unlockCells()
            self.setExploredCells()
            self.evidenceUnlock()
            while(self.change() > c):
                c = self.change()
                self.unlockCells()
                self.setExploredCells()
                self.evidenceUnlock()
            #print(self.chainLength)
        if self.app.isopen:
                   self.app.endpopup("computer won") 

            
     

     
