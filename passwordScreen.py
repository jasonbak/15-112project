#one mode: passwordCreation and passwordEnter

from tkinter import *
import statistics

#REMOVE AFTER DEBUGGING
def passwordScreenResetVariables(data):
    data.glyphCoords = []
    data.strokes = 0
    data.zScoreLog = dict()
    data.password = ""

#modify data from glyph to a standard (set size box located in upper left)
def normalize(data):
    for xCoord in data.xCoords:
        xCoord -= min(data.xCoords)
    for yCoord in data.yCoords:
        yCoord -= min(data.yCoords)

def passwordScreenMousePressed(event, data):
    (x, y) = (event.x, event.y)
    #input box (IB)
    (IBXMid, IBYMid) = (data.width//2, data.IBYMid)
    IBSL = data.IBSideLength
    #done button (DB)
    (DBXMid, DBYMid) = (6*(data.width//8), data.IBYMid+100)
    DBSL = IBSL//2
    #IB
    if(x>IBXMid-IBSL and x<IBXMid+IBSL and y>IBYMid-IBSL and y<IBYMid+IBSL):
        data.strokes += 1
    #DB
    elif(x>DBXMid-DBSL and x<DBXMid+DBSL and y>DBYMid-DBSL and y<DBYMid+DBSL):
        if(data.potentialPassword == data.password):
            data.mode = "welcome"
        else:
            data.potentialPassword = ""
            data.message = "Incorrect password"

def getGlpyhWidth(data):
    return max(data.xCoords) - min(data.xCoords)

def getGlpyhHeight(data):
    return max(data.yCoords) - min(data.yCoords)

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

def getGlyphCoordsAboveCenter(data):
    centerX = statistics.mean(data.xCoords)
    total = 0
    for coord in data.xCoords:
        if(coord > centerX):
            total += 1
    return total

def getGlyphCoordBelowCenter(data):
    centerX = statistics.mean(data.xCoords)
    total = 0
    for coord in data.xCoords:
        if(coord < centerX):
            total += 1
    return total

def getGlyphAboveBelowRatio(data):
    return getGlyphCoordsAboveCenter(data) / getGlyphCoordBelowCenter(data)

def getGlyphCoordsLeftCenter(data):
    centerY = statistics.mean(data.yCoords)
    total = 0
    for coord in data.yCoords:
        if(coord < centerY):
            total += 1
    return total

def getGlyphCoordsRightCenter(data):
    centerY = statistics.mean(data.yCoords)
    total = 0
    for coord in data.yCoords:
        if(coord > centerY):
            total += 1
    return total

def getGlyphLeftRightRatio(data):
    return getGlyphCoordsLeftCenter(data) / getGlyphCoordsRightCenter(data)

#Plugs in glyph data. Then resets glyph data for the next glyph input.
def setGlyphData(data):
    data.xCoords = [coord[0] for coord in data.glyphCoords]
    data.yCoords = [coord[1] for coord in data.glyphCoords]
    data.glyphMeanXcoord = statistics.mean(data.xCoords)
    data.glyphMeanYcoord = statistics.mean(data.xCoords)
    data.glyphWidthHeightRatio = getGlyphWidthHeightRatio(data)
    data.glyphXstartPoint = getGlyphXstartPoint(data)
    data.glyphYstartPoint = getGlyphYstartPoint(data)
    data.glyphXendPoint = getGlyphXendPoint(data)
    data.glyphYendPoint = getGlyphYendPoint(data)
    data.glyphAboveBelowRatio = getGlyphAboveBelowRatio(data)
    data.glyphLeftRightRatio = getGlyphLeftRightRatio(data)
    #reset for the next input
    data.glyphCoords = []
    data.strokes = 0

def determineCharacter(data):
    character = data.password[0]
    lowest = data.zScoreLog[character]
    for char in data.zScoreLog:
        if(data.zScoreLog[char] < lowest):
            lowest = data.zScoreLog[char]
            character = char
    return character

def passwordScreenKeyPressed(event, data):
    if(event.keysym == "Left"):
        data.mode = "usernameInput"
        print('dsfa')
        passwordScreenResetVariables(data)
    elif(event.keysym == "Return"):
        #To avoid empty entries
        #ADD LATER: When height of glyph is 0, program will crash :(
        if(data.glyphCoords == []):
            #data.validEntry isn't used anywhere
            data.validEntry = False
        else:
            setGlyphData(data)
            for char in data.userCharRawData:
                #avoid emptry entries
                if(data.userCharRawData[char]["xCoord"] != []):
                    data.tempZscore += abs(data.glyphMeanXcoord - statistics.mean(data.userCharRawData[char]["xCoord"])) / statistics.pstdev(data.userCharRawData[char]["xCoord"])
                    data.tempZscore += abs(data.glyphMeanYcoord - statistics.mean(data.userCharRawData[char]["yCoord"])) / statistics.pstdev(data.userCharRawData[char]["yCoord"])
                    data.tempZscore += abs(data.glyphWidthHeightRatio - statistics.mean(data.userCharRawData[char]["widthHeightRatio"])) / statistics.pstdev(data.userCharRawData[char]["widthHeightRatio"])
                    data.tempZscore += abs(data.glyphXstartPoint - statistics.mean(data.userCharRawData[char]["xStartPoint"])) / statistics.pstdev(data.userCharRawData[char]["xStartPoint"])
                    data.tempZscore += abs(data.glyphYstartPoint - statistics.mean(data.userCharRawData[char]["yStartPoint"])) / statistics.pstdev(data.userCharRawData[char]["yStartPoint"])
                    data.tempZscore += abs(data.glyphXendPoint - statistics.mean(data.userCharRawData[char]["xEndPoint"])) / statistics.pstdev(data.userCharRawData[char]["xEndPoint"])
                    data.tempZscore += abs(data.glyphYendPoint - statistics.mean(data.userCharRawData[char]["yEndPoint"])) / statistics.pstdev(data.userCharRawData[char]["yEndPoint"])
                    #change to mode of strokes
                    # data.tempZscore += (data.strokes - data.userCharRawData[char]["strokes"]) / data.userCharRawData[char]["strokes"]
                    data.tempZscore += abs(data.glyphAboveBelowRatio - statistics.mean(data.userCharRawData[char]["aboveBelowRatio"])) / statistics.pstdev(data.userCharRawData[char]["aboveBelowRatio"])
                    data.tempZscore += abs(data.glyphLeftRightRatio - statistics.mean(data.userCharRawData[char]["leftRightRatio"])) / statistics.pstdev(data.userCharRawData[char]["leftRightRatio"])
                    
                    data.zScoreLog[char] = data.tempZscore
                    data.tempZscore = 0
            data.potentialPassword += determineCharacter(data)
    elif(event.keysym == "BackSpace"):
        data.potentialPassword = data.password[:-1]

def passwordScreenleftClickMotion(event, data):
    (x, y) = (event.x, event.y)
    (IBXMid, IBYMid) = (data.width//2, data.IBYMid)
    (width, IBSL) = (data.width, data.IBSideLength)
    if(x>IBXMid-IBSL and x<IBXMid+IBSL and y>IBYMid-IBSL and y<IBYMid+IBSL):
        data.glyphCoords.append((event.x, event.y))

def passwordScreenRedrawAll(canvas, data):
    data.IBYMid = 7*(data.height//10)
    canvas.create_rectangle(0,0,data.width, data.height, fill="#252839")
    canvas.create_text(data.width//2, data.height//10,
        text="Please enter your password.", font="Arial 30 bold", fill="#b5b5b7")
    canvas.create_text(data.width//2, 2*(data.height//10),
        text="%s" % (data.potentialPassword), font="Arial 30 bold", fill="#b5b5b7")

    canvas.create_rectangle(6*(data.width//8) - data.IBSideLength, 
        data.IBYMid+100 - data.IBSideLength//2, 6*(data.width//8) + data.IBSideLength,
        data.IBYMid+100 + data.IBSideLength//2, outline="#b5b5b7")
    canvas.create_text(6*(data.width//8), data.IBYMid+100, text="Done!",
        font="Arial 30 bold", fill="#f2b632")

    canvas.create_text(data.width//2, data.height//2, text=data.message, 
        font="Arial 30 bold", fill="#f2b632")

    #Later remove the IB and try to recognize the smallest rextangle formed with each character
    canvas.create_text(data.width//2, 3*(data.height//10),
        text="One character at a time please.", fill="#b5b5b7")
    canvas.create_rectangle((data.width//2) - data.IBSideLength, 
        data.IBYMid - data.IBSideLength, (data.width//2) + data.IBSideLength,
        data.IBYMid + data.IBSideLength, outline="#b5b5b7")