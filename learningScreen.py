#one mode: learning

from tkinter import *
import statistics
import random

def learningScreenResetVariables(data):
    data.charXcoords = []
    data.charYcoords = []
    data.charWidthHeightRatios = []
    data.charXstartPoints = []
    data.charYstartPoints = []
    data.charXendPoints = []
    data.charYendPoints = []
    data.charStrokes = []
    data.glyphCoords = []
    data.strokes = 0

def learningScreenMousePressed(event, data):
    (x, y) = (event.x, event.y)
    #input box (IB)
    (IBXMid, IBYMid) = (data.width//2, data.IBYMid)
    IBSL = data.IBSideLength
    if(x>IBXMid-IBSL and x<IBXMid+IBSL and y>IBYMid-IBSL and y<IBYMid+IBSL):
        data.strokes += 1 

def learningScreenleftClickMotion(event, data):
    (x, y) = (event.x, event.y)
    #input box (IB)
    (IBXMid, IBYMid) = (data.width//2, data.IBYMid)
    IBSL = data.IBSideLength
    if(x>IBXMid-IBSL and x<IBXMid+IBSL and y>IBYMid-IBSL and y<IBYMid+IBSL):
        data.glyphCoords.append((event.x, y))

def learningScreenKeyPressed(event, data):
    if(event.keysym == "Left"):
        data.mode = "home"
        learningScreenResetVariables(data)
    elif(event.keysym == "Return"):
        #When height of glyph is 0, program will crash :(
        if(data.glyphCoords == []):
            data.validEntry = False
        else:
            try:
                incorporateGlyphData(data)
                data.validEntry = True
                if(data.learningTrials == 5):
                    #learned the password
                    if(len(data.strCharToLearn) == 0):
                        incorporateCharacterData(data)
                        index = data.unlearnedCharacters.find(data.currentChar)
                        data.unlearnedCharacters = data.unlearnedCharacters[:index] + data.unlearnedCharacters[index+1:]
                        data.mode = 'home'
                    else:
                        incorporateCharacterData(data)
                        index = data.unlearnedCharacters.find(data.currentChar)
                        data.currentChar = data.strCharToLearn[0]
                        data.strCharToLearn = data.strCharToLearn[1:]
            except:
                print('false')
                data.validEntry = False

#Plugs in glyph data to character data set. Then resets glyph data for the next glyph input.
def incorporateGlyphData(data):
    data.learningTrials += 1
    #data.xCoords and data.yCoords created here
    normalize(data)
    data.charXcoords += data.xCoords
    data.charYcoords += data.yCoords
    data.charWidthHeightRatios.append(getGlyphWidthHeightRatio(data))
    data.charXstartPoints.append(getGlyphXstartPoint(data))
    data.charYstartPoints.append(getGlyphYstartPoint(data))
    data.charXendPoints.append(getGlyphXendPoint(data))
    data.charYendPoints.append(getGlyphYendPoint(data))
    data.charStrokes.append(data.strokes)
    data.charAboveBelowRatio.append(getGlyphAboveBelowRatio(data))
    data.charLeftRightRatio.append(getGlyphLeftRightRatio(data))
    #reset for the next input
    data.glyphCoords = []
    data.strokes = 0

#adjust coords to fit within the set size comparison box
def normalize(data):
    (data.xCoords, data.yCoords) = ([], [])
    (data.tempXCoords, data.tempYCoords) = ([], [])
    for coord in data.glyphCoords:
        data.tempXCoords.append((coord[0]))
        data.tempYCoords.append((coord[1]))
    adjustmentFactor = max(getGlpyhWidth(data), getGlpyhHeight(data)) / data.IBSideLength
    allignBoxLeft = min(data.tempXCoords)
    allignBoxUp = min(data.tempYCoords)
    for coord in data.glyphCoords:
        data.xCoords.append((coord[0] - allignBoxLeft) * adjustmentFactor)
        data.yCoords.append((coord[1] - allignBoxUp) * adjustmentFactor)

#Saves data for the character. Then resets the character data for the next unlearned character.
def incorporateCharacterData(data):
    print(data.currentUserAndPassword)
    print(data.currentChar)
    data.usersRawData[data.currentUserAndPassword][data.currentChar]["xCoord"] = data.charXcoords
    data.usersRawData[data.currentUserAndPassword][data.currentChar]["yCoord"] = data.charYcoords
    data.usersRawData[data.currentUserAndPassword][data.currentChar]["widthHeightRatio"] = data.charWidthHeightRatios
    data.usersRawData[data.currentUserAndPassword][data.currentChar]["xStartPoint"] = data.charXstartPoints
    data.usersRawData[data.currentUserAndPassword][data.currentChar]["yStartPoint"] = data.charYstartPoints
    data.usersRawData[data.currentUserAndPassword][data.currentChar]["xEndPoint"] = data.charXendPoints
    data.usersRawData[data.currentUserAndPassword][data.currentChar]["yEndPoint"] = data.charYendPoints
    data.usersRawData[data.currentUserAndPassword][data.currentChar]["strokes"] = data.charStrokes
    data.usersRawData[data.currentUserAndPassword][data.currentChar]["aboveBelowRatio"] = data.charAboveBelowRatio
    data.usersRawData[data.currentUserAndPassword][data.currentChar]["leftRightRatio"] = data.charLeftRightRatio
    
    #ADD LATER
        #For user recognition, add mode of strokes. If the recognized character doesnt have the same number of stokes as the mode in the training set, then reject password
    #reset for the next unlearned character
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
    data.learningTrials = 0
    data.currentChar = ""

def getGlpyhWidth(data):
    return max(data.tempXCoords) - min(data.tempXCoords)

def getGlpyhHeight(data):
    return max(data.tempYCoords) - min(data.tempYCoords)

def getGlyphWidthHeightRatio(data):
    return getGlpyhWidth(data) / getGlpyhHeight(data)

def getGlyphXstartPoint(data):
    return data.glyphCoords[0][0]

def getGlyphYstartPoint(data):
    return data.glyphCoords[0][1]

def getGlyphXendPoint(data):
    return data.glyphCoords[-1][0]

def getGlyphYendPoint(data):
    return data.glyphCoords[-1][1]

def getGlyphPixelsAboveCenter(data):
    centerX = statistics.mean(data.xCoords)
    total = 0
    for coord in data.xCoords:
        if(coord > centerX):
            total += 1
    return total

def getGlyphPixelsBelowCenter(data):
    centerX = statistics.mean(data.xCoords)
    total = 0
    for coord in data.xCoords:
        if(coord < centerX):
            total += 1
    return total

def getGlyphAboveBelowRatio(data):
    return getGlyphPixelsAboveCenter(data) / getGlyphPixelsBelowCenter(data)

def getGlyphPixelsLeftCenter(data):
    centerY = statistics.mean(data.yCoords)
    total = 0
    for coord in data.yCoords:
        if(coord < centerY):
            total += 1
    return total

def getGlyphPixelsRightCenter(data):
    centerY = statistics.mean(data.yCoords)
    total = 0
    for coord in data.yCoords:
        if(coord > centerY):
            total += 1
    return total

def getGlyphLeftRightRatio(data):
    return getGlyphPixelsLeftCenter(data) / getGlyphPixelsRightCenter(data)

def learningScreenRedrawAll(canvas, data):
    data.IBYMid = 7*(data.height//10)
    canvas.create_rectangle(0,0,data.width, data.height, fill="#252839")
    canvas.create_text(data.width//20, data.height//20,
        text="Learning your: '%s'" %(data.currentChar), anchor=W,
        font="Arial 25", fill="#f2b632")
    if(data.validEntry == False):
        canvas.create_text(data.width//20, 8.5*(data.height//20),
            text="Invalid entry.", anchor=W, fill="#f2b632",
            font="Arial 25 bold")
    canvas.create_text(data.width//20, 2*(data.height//20),
        text="%d inputs left for current character." %(5 - data.learningTrials), 
        font="Arial 25", anchor=W, fill="#f2b632")
    canvas.create_text(data.width//20, 3*(data.height//20),
        text="Characters learned: %s" %(data.learnedChars), 
        font="Arial 20", anchor=W, fill="#b5b5b7")
    canvas.create_text(data.width//20, 4*(data.height//20),
        text="Characters left to learn: %s" %(data.strCharToLearn), 
        font="Arial 20", anchor=W, fill="#b5b5b7")

    #Later remove the box and try to recognize the smallest rextangle formed with each character
    canvas.create_text(data.width//2, 5*(data.height//10),
        text="One character at a time please.", font="Arial 15",
        fill="#b5b5b7")
    canvas.create_rectangle((data.width//2) - data.IBSideLength, 
        data.IBYMid - data.IBSideLength, 
        (data.width//2) + data.IBSideLength,
        data.IBYMid + data.IBSideLength, outline="#b5b5b7")