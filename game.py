#### WITHOUT OPPONENT CODED IN
import tkinter as tk
from tkinter import *
import random
import copy


value_matrix = [[0 for x in range(9)] for y in range(9)]
button_matrix = [[None for x in range(9)] for y in range(9)]
option_matrix1 = [[0 for x in range(3)] for y in range(4)]
option_matrix2 = [[0 for x in range(3)] for y in range(4)]
radio_list = [None for x in range(3)]
root = tk.Tk()
rad_val = tk.IntVar()
rad_val.set(-1)
turn_count = 0
#curr_options = option_matrix[0]
curr_options1 = option_matrix1[0]
curr_options2 = option_matrix2[0]
curr_player = 1
vert_labels = [None for x in range(9)]
hor_labels = [None for x in range(9)]
p1_score = ""
p1_target = ""
p2_score = ""
p2_target = ""
score_labels = [None for x in range(2)]
max_size = 9
rounds = 4
round_start_player = 1
player_labels = [None for x in range(2)]
ended = 0

# number of rounds out of the 12 that are counted
countable_rounds = 11

# 1 for player 1, 2 for player 2 , 0 for draw when filled
result_arr = []

# player option label radio_list

p_opt_labels = [None for x in range(2)]



def main():
    create_all_options()
    render()



def render():
    global rad_val
    global player_labels


    root.title("GOdd Even")

    #display main grid
    for r in range(9):
        for c in range(9):
            b = tk.Button(root, text=value_matrix[r][c],
                borderwidth=1, height = 4, width = 5)
            b.config(command = lambda r=r, c=c, b=b:change_value_matrix(r,c,rad_val.get(), b))
            b.grid(row=r,column=c)

            button_matrix[r][c] = b
            #print(button_matrix)

    #display available options currently with radio
    #buttons which are updated with turns
    display_new_round()
    B = tk.Button(root, text ="Exit")
    B.grid(row=12,column=12)
    B.config(command = quitter)

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
    global p1_target
    global p2_target
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

    p1 = tk.Label(root, text="Player 1 - %s" %(p1_target),
        borderwidth=0, height = 3, width = 15)
    p1.grid(row=3,column=12, columnspan = 2, rowspan = 2)
    player_labels[0]= p1

    p2 = tk.Label(root, text="Player 2 - %s" %(p2_target),
        borderwidth=0, height = 3, width = 15)
    p2.grid(row=5,column=12, columnspan = 2, rowspan = 2)
    player_labels[1] = p2

    player_labels[0].configure(font="sans 16 bold")
    player_labels[1].configure(font="sans 13")

    # render the options_remaining hor_labels
    o1 = tk.Label()



    freeze_allx()
    unfreeze_range(3,6)


    root.mainloop()

#freezes all but the center 3x3 cells
def freeze_all():
    for i in range(0,5):
        for a in looper(i):
            button_matrix[a[0]][a[1]].configure(bg="black", state = "disabled")

def freeze_allx():
    for i in range(0,5):
        for a in looper(i):
            button_matrix[a[0]][a[1]].configure(bg="black", state = "disabled", text = "")




#unfreeze a specific range
def unfreeze_range(x, count):
    if (count == -1):

        for a in looper(x):
            button_matrix[a[0]][a[1]].configure( state = "normal")

    else:
        arr = looper(x)
        print(looper(x))
        chosen = random.sample(arr, 6)

        for a in chosen:
            button_matrix[a[0]][a[1]].configure( state = "normal", text = value_matrix[a[0]][a[1]])


def fix():
    a = root.winfo_geometry().split('+')[0]
    b = a.split('x')
    w = int(b[0])
    h = int(b[1])
    root.geometry('%dx%d' % (w+1,h+1))

def create_all_options():
    global option_matrix1
    global option_matrix2

    total_options = [0,1,2,3,4,5,6,7,8,9,10,11]
    for i in range(0,4):
        for j in range(0,3):
            print(total_options)

            chosen_curr = random.choice(total_options)
            total_options.remove(chosen_curr)
            option_matrix1[i][j] = chosen_curr
            option_matrix2[i][j] = chosen_curr


    #
    # option_matrix1[0][0] = 0
    # option_matrix1[0][1] = 1
    # option_matrix1[0][2] = 1
    # option_matrix1[1][0] = 2
    # option_matrix1[1][1] = 3
    # option_matrix1[1][2] = 3
    # option_matrix1[2][0] = 4
    # option_matrix1[2][1] = 5
    # option_matrix1[2][2] = 5
    # option_matrix1[3][0] = 6
    # option_matrix1[3][1] = 7
    # option_matrix1[3][2] = 7
    #
    # option_matrix2[0][0] = 0
    # option_matrix2[0][1] = 1
    # option_matrix2[0][2] = 1
    # option_matrix2[1][0] = 2
    # option_matrix2[1][1] = 3
    # option_matrix2[1][2] = 3
    # option_matrix2[2][0] = 4
    # option_matrix2[2][1] = 5
    # option_matrix2[2][2] = 5
    # option_matrix2[3][0] = 6
    # option_matrix2[3][1] = 7
    # option_matrix2[3][2] = 7
    #print(option_matrix)



def display_options(opts, root):
    global radio_list
    global p_opt_labels
    for b in radio_list:
        if (b):
            b.grid_forget()

    i= 0
    for a in opts:
        radb = tk.Radiobutton(root,
           text=a,
           padx = 20,
           variable=rad_val,
           value=a)
        radb.grid(row = i, column = 13)
        radio_list.append(radb)


        i = i+1

    p1_optstring = ""
    p2_optstring = ""
    for i in curr_options1:
        p1_optstring = p1_optstring + str(i) + "  "

    for j in curr_options2:
        p2_optstring = p2_optstring + str(j) + "  "

    for k in range(len(player_labels)):
        if (player_labels[k] == None):
            p_opt_labels[k] = tk.Label(root, text = "")
            p_opt_labels[k].grid(row = 4+2*k, column = 15)

    p_opt_labels[0].configure(text = "player1 opts = %s" %(p1_optstring))
    p_opt_labels[1].configure(text = "player2 opts = %s" %(p2_optstring))




def change_value_matrix(r,c,val, b):
    print(r)
    print(c)
    global rad_val
    if (rad_val.get() == -1):
        return
    global turn_count
    global ended
    turn_count = turn_count+1
    if (turn_count//6 >= 4):
        ended=1
        freeze_all()


    #CHANGING AVAILABLE OPTIONS every 6 turns for now
    global curr_options
    global option_matrix
    global value_matrix
    global rounds
    global round_start_player
    global curr_player
    global curr_options2
    global curr_options1
    global player_labels

    value_matrix[r][c] = rad_val.get()
    update_scores()

    #change text of button pressed
    b.config(text = rad_val.get(), font='sans 13 bold', state="disabled")
    print("printing val_matr:\n")
    print(value_matrix)
    #b.config(text = rad_val.get())
    change_sums(r,c)

    # based on current even and odd sum, decides and appends to the result_arr array (0->d, player-1->1, player-2->2)
    if (turn_count%2 == 0):
        record_scores()
        print("recorded_scores:")
        print(result_arr)

    if (turn_count%6 == 0):

        display_new_round()

        rounds = rounds-1
        change_board()


    else:
        if (curr_player == 1):
            print("curr_options1 is:")
            print(curr_options1)
            print("val to remove is:")
            print(rad_val.get())
            curr_options1.remove(rad_val.get())
            print("curr_options1 is after removal:")
            print(curr_options1)
            #displying next players options
            display_options(curr_options2, root)

            #highlight and unhighlight appropriate player: (need to show that player 2 will play next - switching from 1 to 2)
            player_labels[1].configure(font="sans 16 bold")
            player_labels[0].configure(font="sans 13")



        else:
            print("curr_options2 is:")
            print(curr_options2)
            print("val to remove is:")
            print(rad_val.get())
            curr_options2.remove(rad_val.get())
            print("curr_options2 is after removal:")
            print(curr_options2)
            #displying next players options
            display_options(curr_options1, root)

            #highlight and unhighlight appropriate player: (need to show that player 1 will play next - switching from 2 to 1)
            player_labels[0].configure(font="sans 16 bold")
            player_labels[1].configure(font="sans 13")


        rad_val.set(-1)


    #switch players after every turn
    if (curr_player == 1):

        #if starting new round then repeat previous player and highlight appropriately
        if (turn_count%6 == 0):
            player_labels[0].configure(font="sans 16 bold")
            player_labels[1].configure(font="sans 13")
        else:
            #done in "else" since we change only if non-new round
            curr_player = 2
    else:

        #if starting new round then repeat previous player and highlight appropriately
        if (turn_count%6 == 0):
            player_labels[1].configure(font="sans 16 bold")
            player_labels[0].configure(font="sans 13")
        else:
            #done in "else" since we change only if non-new round
            curr_player = 1



def record_scores():
    even_sum = get_even_odd_sums()[0]
    odd_sum = get_even_odd_sums()[1]

    if (even_sum > odd_sum):
        if (p1_target == "even"):
            result_arr.append(1)
        else:
            result_arr.append(2)

    if (odd_sum > even_sum):
        if (p1_target == "odd"):
            result_arr.append(1)
        else:
            result_arr.append(2)

    if (odd_sum == even_sum):
        result_arr.append(0)



def display_new_round():
    global turn_count
    global round_start_player
    global curr_options
    global curr_options1
    global curr_options2
    global root
    global rounds
    global rad_val


    if (turn_count//6 >= 4):
        freeze_all()

    #assigning correct round_starter player since each round alternates
    if (round_start_player == 2):
        round_start_player = 1
    else:
        round_start_player = 2

    curr_options = option_matrix1[turn_count//6]
    curr_options1 = option_matrix1[turn_count//6]
    curr_options2 = option_matrix2[turn_count//6]

    if (round_start_player == 1):
        display_options(curr_options1, root)
    else:
        display_options(curr_options2, root)


    rad_val.set(-1)
    print("did_setup")



def switch_options():
    global rad_val
    played = rad_val.get()


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

    even_sum = get_even_odd_sums()[0]
    odd_sum = get_even_odd_sums()[1]

    # for i in range(max_size):
    #     curr_sum_vert = row_sum(i)
    #     if (curr_sum_vert%2 == 0):
    #         even_sum = even_sum+curr_sum_vert
    #     else:
    #         odd_sum = odd_sum+curr_sum_vert
    #
    #     curr_sum_hor = col_sum(i)
    #     if (curr_sum_hor%2 == 0):
    #         even_sum = even_sum+curr_sum_hor
    #     else:
    #         odd_sum = odd_sum+curr_sum_hor

    if (p1_target == "even"):
        score_labels[0].config(text = even_sum)
        score_labels[1].config(text = odd_sum)
    else:
        score_labels[0].config(text = odd_sum)
        score_labels[1].config(text = even_sum)

#returns an array which returns the sums of the even and odd col and row totals in an array [even_sum, odd_sum]
def get_even_odd_sums():
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

    return [even_sum, odd_sum]

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
    unfreeze_range(rounds-1, 6)


def quitter():
    exit()
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
        if [x,i] not in arr:
            arr.append([x,i])
        if [i,x] not in arr:
            arr.append([i,x])

        if [8-x,i] not in arr:
            arr.append([8-x,i])

        if [i,8-x] not in arr:
            arr.append([i,8-x])

    return arr


























































if __name__ == "__main__":
    main()
