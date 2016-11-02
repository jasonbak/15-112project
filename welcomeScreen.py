from tkinter import *

def welcomeScreenKeyPressed(canvas, data):
    pass
    
def welcomeScreenRedrawAll(canvas, data):
    canvas.create_rectangle(0,0,data.width, data.height, fill="#252839")
    canvas.create_text(data.width//2, data.height//2, text="Welcome, %s!" % (data.currentUser), font="Arial 40", fill="#f2b632")
