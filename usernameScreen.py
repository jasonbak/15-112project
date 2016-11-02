#two modes: usernameCreation and usernameInput

import string
from tkinter import *
import random

def userScreenResetVariables(data):
    data.currentUser = ""
    data.invalidUsername = False

def usernameScreenKeyPressed(event, data):
    if(event.keysym in string.ascii_letters or event.keysym in string.digits):
        data.currentUser += event.keysym
    elif(event.keysym == "BackSpace"):
        data.currentUser = data.currentUser[:len(data.currentUser)-1]
    elif(event.keysym == "Return"):
        if(data.mode == "usernameCreation"):
            data.currentUserAndPassword += data.currentUser + ","
            useSimpleDialogBox(data)
            data.currentUser = ""
        elif(data.mode == "usernameInput"):
            for userAndPassword in data.usersRawData:
                i = userAndPassword.find(",")
                potentialUser = userAndPassword[:i]
                potentialPassword = userAndPassword[i+1:]
                if(data.currentUser == potentialUser):
                    data.password = potentialPassword
                    getUserCharRawData(data)
                    data.mode = "passwordEnter"
            data.invalidUsername = True

    elif(event.keysym == "Left"):
        data.mode = "home"
        userScreenResetVariables(data)

def determineUserExists(data):
    for userAndPassword in data.usersRawData:
        i = userAndPassword.find(",")


def getUserCharRawData(data):
    userAndPassword = data.currentUser + "," + data.password
    data.userCharRawData = data.usersRawData[userAndPassword]

def useSimpleDialogBox(data):
    message = "Create your password using letters or digits. "
    title = "Entering Learning Mode"
    response = simpledialog.askstring(title,message)
    for char in response:
        if(char not in string.ascii_letters and char not in string.digits):
            return useSimpleDialogBox(data)
    data.newPassword = response
    data.currentUserAndPassword += data.newPassword
    data.learnedChars = ""
    data.currentChar = random.choice(data.newPassword)
    for i in range(len(data.newPassword)):
        if(data.currentChar == data.newPassword[i]):
            data.charsToLearn = data.newPassword[:i] + data.newPassword[i+1:]
            data.charsToLearn = list(data.charsToLearn)
            random.shuffle(data.charsToLearn)
            break
    #converts list to a string
    data.strCharToLearn = ""
    for char in data.charsToLearn:
        data.strCharToLearn += char

    if(data.mode == "usernameCreation"):
        if(data.firstUse):
            data.charRawData = dict()
            data.usersRawData = dict()
            for char in data.newPassword:
                data.charRawData[char] = {"xCoord": [], "yCoord": [], "widthHeightRatio": [], "xStartPoint": [], "yStartPoint": [], "xEndPoint": [], "yEndPoint": [], "strokes": [], "aboveBelowRatio": [], "leftRightRatio": []}
            data.usersRawData[data.currentUserAndPassword] =  data.charRawData
            data.firstUse = False
            data.mode = "learning"
        else:
            data.charRawData = dict()
            for char in data.newPassword:
                data.charRawData[char] = {"xCoord": [], "yCoord": [], "widthHeightRatio": [], "xStartPoint": [], "yStartPoint": [], "xEndPoint": [], "yEndPoint": [], "strokes": [], "aboveBelowRatio": [], "leftRightRatio": []}
            data.usersRawData[data.currentUserAndPassword] =  data.charRawData
            data.mode = "learning"

    data.newPassword = ""

def usernameScreenRedrawAll(canvas, data):
    canvas.create_rectangle(0,0,data.width, data.height, fill="#252839")
    if(data.mode == "usernameInput"):
        canvas.create_text(data.width//2, data.height//10,
            text="Please enter your username.", font="Arial 30 bold", fill="#b5b5b7")
    elif(data.mode == "usernameCreation"):
        canvas.create_text(data.width//2, data.height//10,
            text="Please create your username.", font="Arial 30 bold", fill="#b5b5b7")
    canvas.create_rectangle(data.width//4, 16*(data.height//20), 
        3*(data.width//4), 18*(data.height//20))
    canvas.create_text(data.width//2, 17*(data.width//20), 
        text=data.currentUser, font="Arial 20 bold", fill="#f2b632")
    canvas.create_text(data.width//2, 19*(data.width//20),
        text="Press 'Return' to enter your username.", font="Arial 20 bold", fill="#b5b5b7")
    if(data.invalidUsername):
        canvas.create_text(data.width//2, 15*(data.height//20),
            text="Invalid Username", font="Arial 20 bold", fill="#f2b632")