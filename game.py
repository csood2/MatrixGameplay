from tkinter import *


Matrix = [[x+y for x in range(9)] for y in range(9)]


window = Tk()


window.title("Grid Game")


import tkinter
for r in range(9):
    for c in range(9):
        tkinter.Button(window, text=Matrix[r][c],
            borderwidth=1 ).grid(row=r,column=c)
window.mainloop()
