from tkinter import *
import tkinter.messagebox


def createPopUp(errorMsg):
    root=Tk()

    tkinter.messagebox.showinfo('Window Title',errorMsg)