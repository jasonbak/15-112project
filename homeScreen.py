from tkinter import *
from tkinter import simpledialog


def homeScreenKeyPressed(event, data):
    if(event.keysym == "l"):
        data.mode = "usernameInput"
    elif(event.keysym == "r"):
        data.mode = "usernameCreation"

def homeScreenRedrawAll(canvas, data):
    sixth = data.height//12
    canvas.create_rectangle(0,0,data.width, data.height, fill="#252839")
    canvas.create_text(data.width//2, 4*sixth,
        text="Password Protect", font="Arial 40 bold", fill="#f2b632")
    canvas.create_text(data.width//2, 9*sixth,
        text="Press 'l' to log in.", font="Arial 20 bold", fill="#b5b5b7")
    canvas.create_text(data.width//2, 10*sixth,
        text="Press 'r' to register.", font="Arial 20 bold", fill="#b5b5b7")