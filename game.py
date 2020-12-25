import tkinter as tk
from tkinter import *

Matrix = [[x+y for x in range(9)] for y in range(9)]
button_matrix = [[None for x in range(9)] for y in range(9)]
option_matrix = [[0 for x in range(3)] for y in range(4)]

def main():
    create_all_options()
    render()


def render():
    window = Tk()

    window.title("GOdd Even")

    for r in range(9):
        for c in range(9):
            b = tk.Button(window, text=Matrix[r][c],
                borderwidth=1 )
            b.grid(row=r,column=c)

            button_matrix[r][c] = b


    display_options([1,2,3], window)
    window.mainloop()

def create_all_options():
    option_matrix[0][0] = 0
    option_matrix[0][1] = 1
    option_matrix[0][2] = 1
    option_matrix[1][0] = 2
    option_matrix[1][1] = 3
    option_matrix[1][2] = 3
    option_matrix[2][0] = 4
    option_matrix[2][1] = 5
    option_matrix[2][2] = 5
    option_matrix[3][0] = 6
    option_matrix[3][1] = 7
    option_matrix[3][2] = 7
    print(option_matrix)



def display_options(opts, window):
    v = tk.IntVar()
    i= 0
    for a in opts:
        tk.Radiobutton(window,
           text=a,
           padx = 20,
           variable=v,
           value=a).grid(row = i+1, column = 9)

        i = i+1

























































if __name__ == "__main__":
    main()
