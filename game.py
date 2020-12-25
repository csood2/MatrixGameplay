import tkinter as tk
from tkinter import *

value_matrix = [[0 for x in range(9)] for y in range(9)]
button_matrix = [[None for x in range(9)] for y in range(9)]
option_matrix = [[0 for x in range(3)] for y in range(4)]
root = tk.Tk()
rad_val = tk.IntVar()
rad_val.set(-1)
turn_count = 0
curr_options = option_matrix[0]
vert_labels = [None for x in range(9)]
hor_labels = [None for x in range(9)]



def main():
    create_all_options()
    render()



def render():
    global rad_val


    root.title("GOdd Even")

    #display main grid
    for r in range(9):
        for c in range(9):
            b = tk.Button(root, text=value_matrix[r][c],
                borderwidth=1, height = 4, width = 5)
            b.config(command = lambda r=r, c=c, b=b:change_value_matrix(r,c,rad_val.get(), b))
            b.grid(row=r,column=c)

            button_matrix[r][c] = b
            print(button_matrix)

    #display available options currently with radio
    #buttons which are updated with turns
    display_options(curr_options, root)
    B = tk.Button(root, text ="Hello")
    B.grid(row=12,column=12)
    B.config(command = temp)

    #render vertical sum labels
    for i in range(0, 9):
        lab = tk.Label(root, text=row_sum(i),
            borderwidth=1, height = 4, width = 5)
        lab.grid(row=i,column=9)

        vert_labels[i] = lab

    #render horizontal sum labels
    for i in range(0, 9):
        lab = tk.Label(root, text=row_sum(i),
            borderwidth=1, height = 4, width = 5)
        lab.grid(row=9,column=i)

        hor_labels[i] = lab




    root.update()
    root.after(0, fix)

    root.mainloop()



def fix():
    a = root.winfo_geometry().split('+')[0]
    b = a.split('x')
    w = int(b[0])
    h = int(b[1])
    root.geometry('%dx%d' % (w+1,h+1))

def create_all_options():
    global option_matrix

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
    #print(option_matrix)



def display_options(opts, root):

    i= 0
    for a in opts:
        tk.Radiobutton(root,
           text=a,
           padx = 20,
           variable=rad_val,
           value=a).grid(row = i+1, column = 13)

        i = i+1



def change_value_matrix(r,c,val, b):
    print(r)
    print(c)
    global rad_val
    if (rad_val.get() == -1):
        return
    global turn_count
    turn_count = turn_count+1

    #CHANGING AVAILABLE OPTIONS every 6 turns for now
    global curr_options
    global option_matrix
    global value_matrix

    value_matrix[r][c] = rad_val.get()
    b.config(text = rad_val.get())
    print("printing val_matr:\n")
    print(value_matrix)
    #b.config(text = rad_val.get())
    change_sums(r,c)
    if (turn_count%6 == 0):
        curr_options = option_matrix[turn_count//6]
        display_options(curr_options, root)
        rad_val.set(-1)

def change_sums(r,c):
    vert_labels[r].config(text=row_sum(r))
    hor_labels[c].config(text=col_sum(c))



def row_sum(i):
    global value_matrix
    summed = sum(value_matrix[i])

    return summed

def col_sum(i):
    global value_matrix
    summed = sum(row[i] for row in value_matrix)

    return summed


def temp():
    print("doing this")
    global button_matrix
    photo=PhotoImage(file="Black.png")
    button_matrix[1][0].configure(bg="red", state = "disabled")

    print(button_matrix[1][0])

























































if __name__ == "__main__":
    main()
