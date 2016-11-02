#Term Project: PasswordProtect
#Name: Jason Bak
#Andrew ID: jbak1
#Section: I

from passwordScreen import *
from homeScreen import *
from usernameScreen import *
from learningScreen import *
from welcomeScreen import *
from tkinter import *
from tkinter import simpledialog
import string

def init(data):
    data.mode = "home"
    data.fileName = "charData"
    data.unlearnedCharacters = string.ascii_uppercase + string.ascii_lowercase + string.digits

    #usernameScreen
    data.currentUser = ""
    data.currentUserAndPassword = ""
    data.invalidUsername = False

    #passwordScreen
    data.zScoreLog = dict()
    data.potentialPassword = ""
    
    #learningScreen
    data.validEntry = True
    data.learningTrials = 0
    data.charXcoords = []
    data.charYcoords = []
    data.charWidthHeightRatios = []
    data.charXstartPoints = []
    data.charYstartPoints = []
    data.charXendPoints = []
    data.charYendPoints = []
    data.charStrokes = []
    data.charAboveBelowRatio = []
    data.charLeftRightRatio = []

    #passwordScreen + learningScreen
    data.IBSideLength = 50
    data.glyphCoords = []
    data.strokes = 0
    data.tempZscore = 0
    data.message = ""

    readData(data)

def readData(data):
    try:
        with open(data.fileName, "rt") as f:
            data.usersRawData = eval(f.read())
            data.firstUse = False
    #makes data structures
    except:
        data.firstUse = True

def saveData(data):
    with open(data.fileName, "wt") as f:
        #want to add the data into ONE 3d dictionary (2d now, character: characteristics of it) (later add user for 3d)
        f.write(repr(data.usersRawData))

def makeOnClosing(root, data):
    def onClosing():
        saveData(data)
        root.destroy()
    return onClosing

def mousePressed(event, data):
    if(data.mode == "learning"):
        learningScreenMousePressed(event, data)
    elif(data.mode == "passwordCreation" or data.mode == "passwordEnter"):
        passwordScreenMousePressed(event, data)

def keyPressed(event, data):
    if(data.mode == "home"):
        homeScreenKeyPressed(event, data)
    elif(data.mode == "usernameCreation" or data.mode == "usernameInput"):
        usernameScreenKeyPressed(event, data)
    elif(data.mode == "learning"):
        learningScreenKeyPressed(event, data)
    elif(data.mode == "passwordCreation" or data.mode == "passwordEnter"):
        passwordScreenKeyPressed(event, data)
    elif(data.mode == "welcome"):
        welcomeScreenKeyPressed(canvas, data)

#tracks motion of cursor when left-clicked
def leftClickMotion(event, data):
    if(data.mode == "learning"):
        learningScreenleftClickMotion(event, data)
    elif(data.mode == "passwordCreation" or data.mode == "passwordEnter"):
        passwordScreenleftClickMotion(event, data)

def timerFired(data):
    pass

def redrawAll(canvas, data):
    if(data.mode == "home"):
        homeScreenRedrawAll(canvas, data)
    elif(data.mode == "usernameCreation" or data.mode == "usernameInput"):
        usernameScreenRedrawAll(canvas, data)
    elif(data.mode == "learning"):
        learningScreenRedrawAll(canvas, data)
        drawPixels(canvas, data)
    elif(data.mode == "passwordCreation" or data.mode == "passwordEnter"):
        passwordScreenRedrawAll(canvas, data)
        drawPixels(canvas, data)
    elif(data.mode == "welcome"):
        welcomeScreenRedrawAll(canvas, data)

def drawPixels(canvas, data):
    for coord in data.glyphCoords:
        x = coord[0]
        y = coord[1]
        canvas.create_rectangle(x, y, x+5, y+5, width=5, fill="#b5b5b7", outline="#b5b5b7")

####################################
# use the run function as-is
####################################

def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        redrawAll(canvas, data)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def leftClickMotionWrapper(event, canvas, data):
        leftClickMotion(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 100 # milliseconds
    init(data)
    # create the root and the canvas
    root = Tk()
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    root.bind('<B1-Motion>', lambda event:
                            leftClickMotionWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    root.protocol("WM_DELETE_WINDOW", makeOnClosing(root, data))
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

# run(1000, 600)
run(600, 600)