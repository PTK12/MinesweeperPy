import tkinter as tk
import random
import time
import os

#you can change these in the options menu when you run the program
minefieldwidth = 9
minefieldheight = 9
minesonfield = 10 

#FOLDERS
plainpath = os.path.dirname(os.path.abspath(__file__))
folderpaths = ["minetile","faces","timetile","buttontile"]

for i in folderpaths:
    a = i+" = plainpath + '/gif//' + '"+i+"' + '//'"
    exec(a)

#IMAGES
#button
buttonpaths = ["empty","flag","question"]
for i in buttonpaths:
    a = i+'path = os.path.join(buttontile, "'+i+'.gif")'
    exec(a)

#tile
tilepaths1 = ["mine","false","select"]
tilepaths2 = ["mine0","mine1","mine2","mine3","mine4","mine5","mine6","mine7","mine8"]
tilepaths = tilepaths1 + tilepaths2

for i in tilepaths:
    a = i+'path = os.path.join(minetile, "'+i+'.gif")'
    exec(a)

#faces
facepaths = ["happy","lose","tension","cool"]
for i in facepaths:
    a = i+'path = os.path.join(faces, "'+i+'.gif")'
    exec(a)

#num
timepaths = ["time0","time1","time2","time3","time4","time5","time6","time7","time8","time9","timenegative","timenull"]
for i in timepaths:
    a = i+'path = os.path.join(timetile, "'+i+'.gif")'
    exec(a)

allpaths = buttonpaths + tilepaths + facepaths + timepaths

#DATA
#global stuff
time = 0
timer = False

winstate = 0
ObjMinefield = {}
BtnMinefield = {}
AllMines = {}
NonMines = {}

ObjTile = {}
LblTile = {}
AllTile = {}

FlagTile = {}
    
copymine = minesonfield
backupmine = minesonfield
firstclick = False

#classes
class Minefield:
    global minesonfield

    def __init__(self,state,pos,used,alive):
        self.used = used
        self.state = state
        self.pos = pos
        self.alive = alive
    
    def right(self,event):
        
        if self.used == 2:
            self.used = 0
            BtnMinefield[self.pos].configure(image=empty)
            
        elif self.used == 0:
            self.used = 1
            BtnMinefield[self.pos].configure(image=flag)

            FlagTile[self.pos] = BtnMinefield[self.pos]
            updateflag()

            if self.pos in NonMines:
                LblTile[self.pos].configure(image=false)
                
        else:
            FlagTile.pop(self.pos)
            updateflag()
            ObjTile[self.pos].update()
            self.used = 2
            BtnMinefield[self.pos].configure(image=question)
        
    def left(self,event):
        global firstclick, minesonfield

        if firstclick == False:
            firstclick = True

            neighbour = [
            self.pos-minefieldwidth-1,self.pos-minefieldwidth,self.pos-minefieldwidth+1,
            self.pos-1,                                       self.pos+1,
            self.pos+minefieldwidth-1,self.pos+minefieldwidth,self.pos+minefieldwidth+1
            ]

            neighboursideeast = [
            self.pos-minefieldwidth-1,self.pos-minefieldwidth,
            self.pos-1,              
            self.pos+minefieldwidth-1,self.pos+minefieldwidth,
            ]

            neighboursidewest = [
                                      self.pos-minefieldwidth,self.pos-minefieldwidth+1,
                                                              self.pos+1,    
                                      self.pos+minefieldwidth,self.pos+minefieldwidth+1
            ]


            NObjTile = ObjTile.copy()

            if (self.pos+1)%(minefieldwidth) == 0:
                for i in range(minefieldwidth * minefieldheight - copymine):
                    try:
                        if i == 0:
                            NObjTile.pop(self.pos)
                        else:
                            NObjTile.pop(neighboursideeast[i-1])
                    except Exception as e:
                        a = 1

                while minesonfield != 0:
                    for i in NObjTile:   
                        ObjTile[i].randomise()


            elif (self.pos)%(minefieldwidth) == 0:
                for i in range(minefieldwidth * minefieldheight - copymine):
                    try:
                        if i == 0:
                            NObjTile.pop(self.pos)
                        else:
                            NObjTile.pop(neighboursidewest[i-1])
                    except:
                        a = 1

                while minesonfield != 0:
                    for i in NObjTile:   
                        ObjTile[i].randomise()

            else:
                for i in range(minefieldwidth * minefieldheight - copymine):
                    try:
                        if i == 0:
                            NObjTile.pop(self.pos)
                        else:
                            NObjTile.pop(neighbour[i-1])
                    except:
                        a = 1

                while minesonfield != 0:
                    for i in NObjTile:   
                        ObjTile[i].randomise()


            for i in ObjTile:
                ObjTile[i].update()

                if ObjMinefield[i].state == 1:
                    NonMines[i] = ObjMinefield[i]
    
            for i in AllTile:
                LblTile[i].configure(image=mine)

            for i in ObjTile:
                ObjTile[i].update()

        if self.used == 0:
            self.activate()

    def middle(self,event):
        nearbyflags = 0

        if self.alive == 1:
                
            neighbour = [
            self.pos-minefieldwidth-1,self.pos-minefieldwidth,self.pos-minefieldwidth+1,
            self.pos-1,               self.pos,               self.pos+1,
            self.pos+minefieldwidth-1,self.pos+minefieldwidth,self.pos+minefieldwidth+1
            ]

            neighboursideeast = [
            self.pos-minefieldwidth-1,self.pos-minefieldwidth,
            self.pos-1,               self.pos,
            self.pos+minefieldwidth-1,self.pos+minefieldwidth,
            ]

            neighboursidewest = [
                                      self.pos-minefieldwidth,self.pos-minefieldwidth+1,
                                      self.pos,               self.pos+1,    
                                      self.pos+minefieldwidth,self.pos+minefieldwidth+1
            ]
            
            if (self.pos+1)%(minefieldwidth) == 0:
                for i in neighboursideeast:
                    if i in FlagTile:
                        nearbyflags += 1

                if (ObjTile[self.pos].surround - nearbyflags) == 0:
                    
                    for i in neighboursideeast:
                        
                        if i not in FlagTile and i in ObjTile:
                            ObjMinefield[i].activate()
                        
            elif (self.pos)%(minefieldwidth) == 0:
                for i in neighboursidewest:
                    if i in FlagTile:
                        nearbyflags += 1

                if (ObjTile[self.pos].surround - nearbyflags) == 0:
                    for i in neighboursidewest:
                        if i not in FlagTile and i in ObjTile:
                            ObjMinefield[i].activate()

            else:
                for i in neighbour:
                    if i in FlagTile:
                        nearbyflags += 1

                if (ObjTile[self.pos].surround - nearbyflags) == 0:
                    for i in neighbour:
                        if i not in FlagTile and i in ObjTile:
                            ObjMinefield[i].activate()

    def activate(self):
        global timer

        if timer == False:
            timer = True
        
        if self.alive == 0:
            
            if ObjMinefield[self.pos].state == 1:
                NonMines.pop(self.pos)
                BtnMinefield[self.pos].grid_forget()

                if ObjTile[self.pos].surround == 0:
                    self.autoactivate()


            else:
                self.destroy()

        self.alive = 1
        if not bool(NonMines):
            win()

    def destroy(self):
        global winstate
        winstate = -1
        face.configure(image=lose)
        for i in FlagTile:
            FlagTile[i].grid_forget()
            
        for i in AllTile:
            BtnMinefield[i].grid_forget()
            LblTile[i].configure(image=mine)
            
        for i in BtnMinefield:
            BtnMinefield[i].unbind('<Button-1>')
            BtnMinefield[i].unbind('<Button-3>')
            BtnMinefield[i].unbind('<Button-2>')
        LblTile[self.pos].configure(image=select)

    def buttonise(self):
        BtnMinefield[self.pos] = tk.Button(maingrid,image=empty,borderwidth=1,bg="#c0c0c0")
            
        BtnMinefield[self.pos].bind('<Button-1>', self.left) 
        BtnMinefield[self.pos].bind('<Button-3>', self.right)
        LblTile[self.pos].bind('<Button-2>', self.middle)

    def autoactivate(self):

        if self.alive == 0:
            if self.pos in NonMines:
                NonMines.pop(self.pos)
                
            BtnMinefield[self.pos].grid_forget()
            self.alive = 1

            neighbour = [
            self.pos-minefieldwidth-1,self.pos-minefieldwidth,self.pos-minefieldwidth+1,
            self.pos-1,               self.pos,               self.pos+1,
            self.pos+minefieldwidth-1,self.pos+minefieldwidth,self.pos+minefieldwidth+1
            ]

            neighboursideeast = [
            self.pos-minefieldwidth-1,self.pos-minefieldwidth,
            self.pos-1,               self.pos,
            self.pos+minefieldwidth-1,self.pos+minefieldwidth,
            ]

            neighboursidewest = [
                                      self.pos-minefieldwidth,self.pos-minefieldwidth+1,
                                      self.pos,               self.pos+1,    
                                      self.pos+minefieldwidth,self.pos+minefieldwidth+1
            ]
            
            if ObjTile[self.pos].surround == 0:
                if (self.pos+1)%(minefieldwidth) == 0:
                    for i in neighboursideeast:
                        if i in ObjTile:
                            ObjMinefield[i].autoactivate()
                            
                elif (self.pos)%(minefieldwidth) == 0:
                    for i in neighboursidewest:
                        if i in ObjTile:
                            ObjMinefield[i].autoactivate()

                else:
                    for i in neighbour:
                        if i in ObjTile:
                            ObjMinefield[i].autoactivate()

        if not bool(NonMines):
            win()
class Tile:
    #LblTile[self.pos]
    def __init__(self,state,pos,surround):
        self.state = state
        self.pos = pos
        self.surround = surround

    def labelise(self):
        LblTile[self.pos] = tk.Label(maingrid,bg="#c0c0c0")
        if ObjTile[self.pos].state == False:
            LblTile[self.pos].configure(image=mine)

    def randomise(self):
        global minesonfield,copymine

        if self.state == True:
            if minesonfield > 0:
                if random.randint(1,copymine) == 1:
                    AllTile[self.pos] = LblTile[self.pos]
                    AllTile[self.pos].configure(image=mine)
                    self.state = False
                    ObjMinefield[self.pos].state = 0
                    AllMines[self.pos] = ObjMinefield[self.pos]
                    minesonfield -= 1

    def update(self):
        global minefieldwidth

        self.surround = 0

        neighbour = [
        self.pos-minefieldwidth-1,self.pos-minefieldwidth,self.pos-minefieldwidth+1,
        self.pos-1,               self.pos,               self.pos+1,
        self.pos+minefieldwidth-1,self.pos+minefieldwidth,self.pos+minefieldwidth+1
        ]

        neighboursideeast = [
        self.pos-minefieldwidth-1,self.pos-minefieldwidth,
        self.pos-1,               self.pos,
        self.pos+minefieldwidth-1,self.pos+minefieldwidth,
        ]

        neighboursidewest = [
                                  self.pos-minefieldwidth,self.pos-minefieldwidth+1,
                                  self.pos,               self.pos+1,    
                                  self.pos+minefieldwidth,self.pos+minefieldwidth+1
        ]

        if self.state == True:
            if (self.pos+1)%(minefieldwidth) == 0:
                for i in neighboursideeast:
                    if i in AllMines:
                        self.surround += 1
                        
            elif (self.pos)%(minefieldwidth) == 0:
                for i in neighboursidewest:
                    if i in AllMines:
                        self.surround += 1

            else:
                for i in neighbour:
                    if i in AllMines:
                        self.surround += 1

            LblTile[self.pos].configure(image=minevalue[self.surround])
    
        
root = tk.Tk()
root.title('Minesweeper Py')
root.configure(background='#c0c0c0')

#I couldve simplified this more but who cares
for i in allpaths:
    a = i + ' = tk.PhotoImage(file = '+ i + 'path)'
    exec(a)

root.tk.call('wm', 'iconphoto', root._w, mine)

#easier to find later
minevalue = [mine0,mine1,mine2,mine3,mine4,mine5,mine6,mine7,mine8,false,mine,select,empty,happy,lose,cool]
timelist = [time0,time1,time2,time3,time4,time5,time6,time7,time8,time9,timenegative,timenull]

space = tk.Frame(root,bg="#c0c0c0",borderwidth=3,relief="sunken")
space.grid(row=0,column=0,sticky="we",padx=5,pady=5)


#1
flagsdisplay = tk.Frame(space,bg="#c0c0c0",highlightthickness=0)
flagsdisplay.grid(row=0,column=1)

digit1 = tk.Label(flagsdisplay,image=timelist[0],highlightthickness=0,bg="#c0c0c0")
digit1.pack(side="left",padx=0,pady=0)

digit2 = tk.Label(flagsdisplay,image=timelist[0],highlightthickness=0,bg="#c0c0c0")
digit2.pack(side="left",padx=0,pady=0)

digit3 = tk.Label(flagsdisplay,image=timelist[0],highlightthickness=0,bg="#c0c0c0")
digit3.pack(side="left",padx=0,pady=0)

#2
gap1 = tk.Label(space,bg="#c0c0c0")
gap1.grid(row=0,column=2)

#3
face = tk.Button(space,image=happy,command=lambda:go(),bg="#c0c0c0",borderwidth=3)
face.grid(row=0,column=3,pady=5)

#4
gap2 = tk.Label(space,bg="#c0c0c0")
gap2.grid(row=0,column=4)

#5
timedisplay = tk.Frame(space,bg="#c0c0c0")
timedisplay.grid(row=0,column=5)

digit4 = tk.Label(timedisplay,image=timelist[0],highlightthickness=0,bg="#c0c0c0")
digit4.pack(side="left",padx=0,pady=0)

digit5 = tk.Label(timedisplay,image=timelist[0],highlightthickness=0,bg="#c0c0c0")
digit5.pack(side="left",padx=0,pady=0)

digit6 = tk.Label(timedisplay,image=timelist[0],highlightthickness=0,bg="#c0c0c0")
digit6.pack(side="left",padx=0,pady=0)


space.columnconfigure(2,weight=1)
space.columnconfigure(4,weight=1)

maingrid = tk.Frame(root,borderwidth=3,relief="sunken")
maingrid.grid(row=1,column=0,padx=5,pady=5)

savespace = tk.Label(root)

#stops images disappearing (idk why python does this)
for i in minevalue:
    savespace.configure(image=i)

def win():
    global winstate,cool
    if winstate == 0:
        face.configure(image=cool)
        winstate = 1

        for i in BtnMinefield:
            BtnMinefield[i].unbind('<Button-1>')
            BtnMinefield[i].unbind('<Button-2>')

def go():
    global winstate,minesonfield,copymine,backupmine,timer,time,firstclick
    
    face.configure(image=happy)
    digit4.configure(image=timelist[0])
    digit5.configure(image=timelist[0])
    digit6.configure(image=timelist[0])

    time = 0
    timer = False

    winstate = 0
    minesonfield = copymine
    ObjMinefield.clear()
    BtnMinefield.clear()
    AllMines.clear()
    NonMines.clear()

    ObjTile.clear()
    LblTile.clear()
    AllTile.clear()

    FlagTile.clear()

    firstclick = False

    for i in maingrid.winfo_children():
        i.destroy()

    for i in range((minefieldwidth)*(minefieldheight)):

        ObjTile[i] = Tile(True,i,0)
        ObjTile[i].labelise()

        LblTile[i].grid(row=i//minefieldwidth,column=i%minefieldwidth)
        LblTile[i].configure(borderwidth=0)
        LblTile[i].configure(image=empty)


        ObjMinefield[i] = Minefield(1,i,0,0)
        ObjMinefield[i].buttonise()
        
        BtnMinefield[i].image = empty
        BtnMinefield[i].grid(row=i//minefieldwidth,column=i%minefieldwidth)

    updateflag()

def timeclock():
    global timer,time,winstate

    if winstate == 0:
        
        if time == 999:
            timer = False
        
        if timer:
            time += 1

            num4 = (time % 1000) // 100
            num5 = (time % 100)  // 10
            num6 = (time % 10)   // 1

            digit4.configure(image=timelist[num4])
            digit5.configure(image=timelist[num5])
            digit6.configure(image=timelist[num6])

    root.after(1000,timeclock)

def updateflag():
    global copymine
    
    activeflags = 0
    
    for i in FlagTile:
        activeflags += 1

    flagnum = copymine - activeflags

    num1 = (flagnum % 1000) // 100
    num2 = (flagnum % 100)  // 10
    num3 = (flagnum % 10)   // 1

    if flagnum < 0:
        num0 = -(flagnum % 100)

        num1 = 10
        num2 = (num0 % 100) // 10
        num3 = (num0 % 10)  // 1
        

    digit1.configure(image=timelist[num1])
    digit2.configure(image=timelist[num2])
    digit3.configure(image=timelist[num3])



go()
timeclock()

def sett():
    global minefieldheight, minefieldwidth, copymine

    def savemine():
        global minefieldheight, minefieldwidth, copymine

        optionstate = v.get()
        
        if optionstate != 3:
            minelist = [
            [9 ,9 ,10],
            [16,16,40],
            [16,30,99],
            ]

            minefieldheight, minefieldwidth, copymine = minelist[optionstate]

        else:
            a = settlength.get()
            b = settwidth.get()
            c = settmine.get()

            if a.isdigit() and b.isdigit() and c.isdigit():
                a,b,c = int(a),int(b),int(c)

                if a > 24:
                    a = 24
                if a < 9:
                    a = 9
                if b > 30:
                    b = 30
                if b < 9:
                    b = 9
                if c > 668:
                    c = 668
                if c < 10:
                    c = 10

                if c > (a*b):
                    c = (a*b)

                minefieldheight, minefieldwidth, copymine = a,b,c

        go()

        settingstuff.destroy()
    difficulty = [
        ("Beginner"),
        ("Intermediate"),
        ("Expert"),
        ("Custom"),
    ]

    settingstuff = tk.Tk()
    settingstuff.title("Options")

    v = tk.IntVar(settingstuff)

    for val, mode in enumerate(difficulty):
        stuff = tk.Radiobutton(
                settingstuff,
                text = mode,
                padx = 20, 
                variable = v,
                value = val
                )
        stuff.grid(column=val//3, row=((val*2)+1)%6, sticky = "nw")
        stuff.select()

    BeginnerD = tk.Label(settingstuff,
        text="""
        10 mines
        9 x 9 tile grid
        """,
        anchor="w")
    BeginnerD.grid(column=0,row=2,sticky="nw")

    IntermediateD = tk.Label(settingstuff,
        text="""
        40 mines
        16 x 16 tile grid
        """,
        anchor="w")
    IntermediateD.grid(column=0,row=4,sticky="nw")

    ExpertD = tk.Label(settingstuff,
        text="""
        99 mines
        16 x 30 tile grid
        """,
        anchor="w")
    ExpertD.grid(column=0,row=6,sticky="nw")

    heightlabel = tk.Label(settingstuff,text="Height (9-24)")
    heightlabel.grid(column=1,row=2,sticky="w")

    widthlabel = tk.Label(settingstuff,text="Width (9-30)")
    widthlabel.grid(column=1,row=3,sticky="w")

    minelabel = tk.Label(settingstuff,text="Mines (10-668)")
    minelabel.grid(column=1,row=4,sticky="w")

    errorlabel = tk.Label(settingstuff,text="(Values will be capped if out of range)")
    errorlabel.grid(column=1,row=5,sticky="w")

    savebutton = tk.Button(settingstuff,text="Save",width=16,command=lambda:savemine())
    savebutton.grid(column=1,row=6,sticky="w")

    settlength = tk.Entry(settingstuff)
    settlength.grid(column=3,row=2,sticky="w")
    settlength.insert(0,minefieldheight)

    settwidth = tk.Entry(settingstuff)
    settwidth.grid(column=3,row=3,sticky="w")
    settwidth.insert(0,minefieldwidth)

    settmine = tk.Entry(settingstuff)
    settmine.grid(column=3,row=4,sticky="w")
    settmine.insert(0,copymine)
    
menubar = tk.Menu(root)

gamemenu = tk.Menu(menubar, tearoff=0)
gamemenu.add_command(label="New Game", command=go)
gamemenu.add_separator()
gamemenu.add_command(label="Options", command=sett)
gamemenu.add_separator()
gamemenu.add_command(label="Exit", command=root.quit)
menubar.add_cascade(label="Game", menu=gamemenu)

helpmenu = tk.Menu(menubar, tearoff=0)
helpmenu.add_command(label="¯\\_(ツ)_/¯")
helpmenu.add_command(label="Look for tutorials online")
helpmenu.add_separator()
helpmenu.add_command(label="This is a work in progress!")
helpmenu.add_separator()
helpmenu.add_command(label="Minesweeper has way too many features")
helpmenu.add_command(label="so I reduced it to make it")
helpmenu.add_command(label="easier for me to make")
menubar.add_cascade(label="Help", menu=helpmenu)

root.config(menu=menubar)

root.mainloop()
