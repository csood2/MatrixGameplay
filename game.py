import tkinter as tk
from tkinter import *
import random


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
p1_score = ""
p1_target = ""
p2_score = ""
p2_target = ""
score_labels = [None for x in range(2)]
max_size = 9
rounds = 4



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

    #Create player score section
    foo = [0,1]
    if (random.choice(foo) == 0):
        p1_target = "even"
        p2_target = "odd"
    else:
        p1_target = "odd"
        p2_target = "even"

    score_labels[0] = tk.Label(root, text=0,
        borderwidth=0, height = 4, width = 5)
    score_labels[0].grid(row=4,column=12, columnspan = 2)

    score_labels[1] = tk.Label(root, text=0,
        borderwidth=0, height = 4, width = 5)
    score_labels[1].grid(row=6,column=12, columnspan = 2)

    tk.Label(root, text="Player 1 - %s" %(p1_target),
        borderwidth=0, height = 4, width = 10).grid(row=3,column=12, columnspan = 2, rowspan = 2)

    tk.Label(root, text="Player 2 - %s" %(p2_target),
        borderwidth=0, height = 4, width = 10).grid(row=5,column=12, columnspan = 2, rowspan = 2)



    freeze_all()
    unfreeze_range(3)


    root.mainloop()

#freezes all but the center 3x3 cells
def freeze_all():
    for i in range(0,5):
        for a in looper(i):
            button_matrix[a[0]][a[1]].configure(bg="black", state = "disabled")




#unfreeze a specific range
def unfreeze_range(x):
    for a in looper(x):
        button_matrix[a[0]][a[1]].configure(bg="black", state = "normal")




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
           value=a).grid(row = i, column = 13)

        i = i+1



def change_value_matrix(r,c,val, b):
    print(r)
    print(c)
    global rad_val
    if (rad_val.get() == -1):
        return
    global turn_count
    turn_count = turn_count+1
    if (turn_count//6 >= 4):
        freeze_all()

    #CHANGING AVAILABLE OPTIONS every 6 turns for now
    global curr_options
    global option_matrix
    global value_matrix
    global rounds

    value_matrix[r][c] = rad_val.get()
    b.config(text = rad_val.get())
    print("printing val_matr:\n")
    print(value_matrix)
    #b.config(text = rad_val.get())
    change_sums(r,c)
    if (turn_count%6 == 0):
        if (turn_count//6 >= 4):
            freeze_all()

        curr_options = option_matrix[turn_count//6]
        display_options(curr_options, root)
        rounds = rounds-1
        change_board()
        rad_val.set(-1)

    update_scores()

def change_sums(r,c):
    vert_labels[r].config(text=row_sum(r))
    hor_labels[c].config(text=col_sum(c))


def update_scores():
    global p1_score
    global p1_target
    global p2_score
    global p2_target
    global max_size
    global score_labels

    even_sum = 0
    odd_sum = 0

    for i in range(max_size):
        curr_sum_vert = row_sum(i)
        if (curr_sum_vert%2 == 0):
            even_sum = even_sum+curr_sum_vert
        else:
            odd_sum = odd_sum+curr_sum_vert

        curr_sum_hor = col_sum(i)
        if (curr_sum_hor%2 == 0):
            even_sum = even_sum+curr_sum_hor
        else:
            odd_sum = odd_sum+curr_sum_hor

    if (p1_target == "even"):
        score_labels[0].config(text = even_sum)
        score_labels[1].config(text = odd_sum)
    else:
        score_labels[0].config(text = odd_sum)
        score_labels[1].config(text = even_sum)

#calculates sum of given row
def row_sum(i):
    global value_matrix
    summed = sum(value_matrix[i])

    return summed

#calculates sum of given col
def col_sum(i):
    global value_matrix
    summed = sum(row[i] for row in value_matrix)

    return summed

def change_board():
    global rounds
    freeze_all()
    unfreeze_range(rounds-1)


def temp():
    print("doing this")
    global button_matrix
    photo=PhotoImage(file="Black.png")
    button_matrix[1][0].configure(bg="red", state = "disabled")

    #print(button_matrix[1][0])
    print(looper(1))
    for a in looper(1):
        button_matrix[a[0]][a[1]].configure(bg="black", state = "disabled")

def looper(x):
    arr = []
    for i in range (0+x,9-x):
        arr.append([x,i])
        arr.append([i,x])
        arr.append([8-x,i])
        arr.append([i,8-x])

    return arr


























































if __name__ == "__main__":
    main()
