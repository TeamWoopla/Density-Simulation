import random
import tkinter as tk

### CANVAS   ###

# creating the window
root = tk.Tk()
root.title("Density Simulation")
root.geometry("%dx%d+%d+%d" % (1200, 800, 50, 100))
canvas = tk.Canvas(root, width=1200, height=800)
canvas.pack()

# creating the layout
WaterY = 500
WaterX = 290
Water = canvas.create_rectangle(1200, 800, WaterX, WaterY, fill="blue")
Side = canvas.create_rectangle(0, 0, 300, 800, fill="#c4c4c4")

###   CANVAS   ###

###   ENTRIES && LABELS   ###

# creating the input-boxes and labels lists
Entrys = []
Lables = []

''' What every num defines
  0. Liquid Density
  1. Liquid Height
  2. Object Mass
  3. Object Volume
  4. Object Density
  5. Object Color
'''

# setting the input-boxes and labels Tests
Titles = ["Liquid Density", "Liquid Height", "Object Mass", "Object Volume", "Object Density", "Object Color"]
Arguments = ["1.0", str(WaterY), "None", "None", "None", "#None"]

# creating the input-boxes and labels
for i in range(6):
    if i in [4, 5]:
        Entrys.append(tk.Label(root, text="0"))
        Entrys[i].config(font=("Courier", 15))
        Entrys[i].place(x=40, y=70 + 90 * i)
    else:
        Entrys.append(tk.Entry(root))
        Entrys[i].place(x=40, y=70 + 90 * i, width=220, height=30)
        Entrys[i].config(font=("Courier", 20))
        Entrys[i].insert(0, Arguments[i])

    Lables.append(tk.Label(root, text=Titles[i] + " : "))
    Lables[i].config(font=("Courier", 15))
    Lables[i].place(x=40, y=30 + i * 90)


###   ENTRIES && LABELS   ###

###   Objects && Functions   ###

# an Object class defines every rectangle on the screen has 12 parameters that's used to draw the rectangle and implements physics
class Object:

    # default values for the variables
    def __init__(self, Mass=2.0, Volume=2.0, Density=1.0, Color="#fff", X=500, Y=200, Flying=False):

        self.Mass = Mass
        self.Volume = Volume
        self.Density = Density
        self.DensityIn = Density
        self.Color = Color
        self.X = X
        self.Y = Y
        self.Width = 100
        self.Height = 100
        self.Speed = 1
        self.Flying = Flying
        self.HightLight = False

        self.Rectangle = canvas.create_rectangle(self.X, self.Y, self.X + self.Width, self.Y + self.Height,
                                                 fill=self.Color, outline=self.Color, width=7)

    # a change function for every variable, if a protocol is needed
    def Change(self, NewAmount, Parmeter="Mass"):
        if Parmeter == "Mass":
            self.Mass = NewAmount
            self.Density = self.Mass / self.Volume
            self.ChangeSpeed()
        elif Parmeter == "Volume":
            if NewAmount not in [0, 0.0]:
                self.Volume = NewAmount
                self.Density = self.Mass / self.Volume
                self.ChangeSpeed()
        elif Parmeter == "Density":
            self.Density = NewAmount
            self.Mass = self.Density * self.Volume
            self.ChangeSpeed()
        elif Parmeter == "DensityIn":
            self.DensityIn = NewAmount
            self.ChangeSpeed()
        elif Parmeter == "Color":
            self.Color = NewAmount
        elif Parmeter == "X":
            self.X = NewAmount
        elif Parmeter == "Y":
            self.Y = NewAmount
        elif Parmeter == "Height":
            self.Height = NewAmount
        elif Parmeter == "Width":
            self.Width = NewAmount

    # moving the object by the SpeedD, Density and LqDensity
    def Physics(self):
        global WaterY
        if not self.Flying:
            if self.Y < WaterY - self.Height / 2:
                self.Y += 15
            else:
                if self.Y + self.Speed + self.Height > root.winfo_height():
                    self.Y = root.winfo_height() - self.Height
                elif self.Y + self.Speed < WaterY - self.Height / 2:
                    self.Y = WaterY - self.Height / 2
                else:
                    self.Y += self.Speed

    # redraw the rectangle
    def Draw(self):
        canvas.coords(self.Rectangle, self.X, self.Y, self.X + self.Width, self.Y + self.Height)
        if self.HightLight:
            canvas.itemconfig(self.Rectangle, outline="#33FF00")
        else:
            canvas.itemconfig(self.Rectangle, outline=self.Color)

    # if the object intersects with a x,y or an object - the object part isn't used un this version
    def Intersects(self, X=50, Y=50, AObject=None):
        if AObject is None:
            if self.X < X < self.X + self.Width and self.Y < Y < self.Y + self.Height:
                return True
        else:
            if ((self.X > AObject.X + AObject.Width) or (self.X + self.Width < AObject.X) or
                    (self.Y > AObject.Y + AObject.Height) or (self.Y + self.Height < AObject.Y)):
                return False
            return True
        return False

    # changing the speed relative form the Density and LqDensity
    def ChangeSpeed(self):
        if self.DensityIn in [self.Density, 0, 0.0] or self.Density in [0, 0.0]:
            self.Speed = 0
        elif self.Density < self.DensityIn:
            self.Speed = -(self.DensityIn / self.Density)
        elif self.Density > self.DensityIn:
            self.Speed = self.Density / self.DensityIn


# a cool function that's removes the letters and symbols from a string and give back an float and bool to detect
def IsFloat(Float):
    FList = [Dig for Dig in str(Float) if Dig in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "."]]
    if not FList == []:
        if not (FList.count(".") > 1 or "." in [FList[0], FList[-1]]):
            NFloat = ""
            for Dig in FList:
                NFloat += Dig
            return [True, float(NFloat)]
    return [False, ""]


# create a random object with random parameters
def RandObject():
    RColor = "%06x" % random.randint(0, 0xFFFFFF)
    RM, RV = float(random.randint(1, 10)), float(random.randint(1, 10))
    Objects.append(Object(X=100, Y=600, Color=f"#{RColor}", Flying=True, Mass=RM, Volume=RV))


###   Objects && Functions   ###

###   Arguments   ###

OM, OV, LD, OD = 0, 0, 0, 0

Clicked = False
FirstStick = False
Moving = False
Objects = []
ObjectChose = -1

RandObject()


###   Arguments   ###

###   Mouse   ###


# if the mouse is pressed an Clicked bool is True
def Mouse(event, Click):
    global Clicked
    Clicked = Click


root.bind('<Button-1>', lambda event: Mouse(event, True))
root.bind('<ButtonRelease-1>', lambda event: Mouse(event, False))


###   Mouse   ###

###  Main While Loop   ###


def Loop():
    # input and refreshing variables
    global OM, OV, OD, LD, ObjectChose, Clicked, FirstStick, Moving, WaterY
    OM, OV, LD = Entrys[2].get(), Entrys[3].get(), Entrys[0].get()
    MouseX = root.winfo_pointerx() - root.winfo_rootx()
    MouseY = root.winfo_pointery() - root.winfo_rooty()

    # calculating the density
    if IsFloat(OV)[0] and IsFloat(OM)[0] and not (0.0 in [IsFloat(OM)[1], IsFloat(OV)[1]]):
        OD = str(IsFloat(OM)[1] / IsFloat(OV)[1])
    else:
        OD = "Null"

    # setting the chosen Object with the new parameters
    if IsFloat(OV)[0]:
        Objects[ObjectChose].Change(IsFloat(OV)[1], "Volume")
    if IsFloat(OM)[0]:
        Objects[ObjectChose].Change(IsFloat(OM)[1], "Mass")

    # refreshing the labels and water
    Entrys[4].config(text=str(OD))
    if IsFloat(Entrys[1].get())[0]:
        WaterY = root.winfo_height() - int(IsFloat(Entrys[1].get())[1])
        if WaterY < 70:
            WaterY = 70
        canvas.coords(Water, 1200, 800, WaterX, WaterY)

    # refreshing the objects
    for ObjP in range(len(Objects)):
        Objects[ObjP].Physics()
        Objects[ObjP].Draw()
        if IsFloat(LD)[0] and IsFloat(LD)[1] is not None:
            Objects[ObjP].Change(IsFloat(LD)[1], "DensityIn")

        # checking for a new height-lighted object and replacing it
        if Objects[ObjP].Intersects(MouseX, MouseY) and not Clicked and not FirstStick:
            if ObjectChose != ObjP:
                Objects[ObjectChose].HightLight = False
                Objects[ObjP].HightLight = True
                Entrys[2].delete(0, 'end')
                Entrys[2].insert(0, str(Objects[ObjP].Mass))
                Entrys[3].delete(0, 'end')
                Entrys[3].insert(0, str(Objects[ObjP].Volume))
                Entrys[5].config(text=Objects[ObjP].Color)
            ObjectChose = ObjP

    # if the mouse is intersecting and clicked start moving the object
    if Clicked and Objects[ObjectChose].Intersects(MouseX, MouseY):
        Moving = True
    if not Clicked:
        Moving = False

    # change the object x,y relative to the mouse position and not out of bounds
    if Moving and not FirstStick:
        Objects[ObjectChose].Flying = True
        if ObjectChose == len(Objects) - 1:
            FirstStick = True
        else:
            if MouseX <= WaterX + 10:
                Objects[ObjectChose].Change(WaterX + 10, "X")
            elif MouseX >= root.winfo_width() - Objects[ObjectChose].Width:
                Objects[ObjectChose].Change(root.winfo_width() - Objects[ObjectChose].Width, "X")
            else:
                Objects[ObjectChose].Change(MouseX, "X")
            if MouseY <= 0:
                Objects[ObjectChose].Change(0, "Y")
            elif MouseY >= root.winfo_height() - Objects[ObjectChose].Height:
                Objects[ObjectChose].Change(root.winfo_height() - Objects[ObjectChose].Height, "Y")
            else:
                Objects[ObjectChose].Change(MouseY, "Y")

    # if the object click is the last in the list(the new one) don't let the user place it out side the bounds
    if FirstStick:
        Objects[ObjectChose].Change(MouseX, "X")
        Objects[ObjectChose].Change(MouseY, "Y")
        if WaterX < MouseX < root.winfo_width() and 0 < MouseY < root.winfo_height():
            FirstStick = False
            RandObject()

    if not ObjectChose == len(Objects) - 1 and not Clicked and ObjectChose >= 0:
        Objects[ObjectChose].Flying = False

    # loop the loop :D
    root.after(50, Loop)


# start the loop
root.after(50, Loop)
root.resizable(False, False)
root.mainloop()

###   Main While Loop   ###
