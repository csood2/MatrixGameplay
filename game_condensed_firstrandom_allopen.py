#### WITH OPPONENT CODED IN

import tkinter as tk
from tkinter import *
from tkinter.messagebox import showinfo

import random
import copy
import time

#num_open is the number of open slots initially in each printing
num_open = 10

#stays the same
total_rounds = 4


value_matrix = [[0 for x in range(9)] for y in range(9)]
button_matrix = [[None for x in range(9)] for y in range(9)]
option_matrix1 = [[0 for x in range(num_open//2)] for y in range(total_rounds)]
option_matrix2 = [[0 for x in range(num_open//2)] for y in range(total_rounds)]
radio_list = [None for x in range(num_open//2)]
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

#increaeses with each round change
rounds = 2
round_start_player = 1
player_labels = [None for x in range(2)]
ended = 0

auto_player = 2


# number of rounds out of the 12 that are counted
countable_rounds = 11

# 1 for player 1, 2 for player 2 , 0 for draw when filled
result_arr = []

# player option label radio_list
p_opt_labels = [None for x in range(2)]

# stores currently open buttons (array of x,y) pair arrays
# has num_open rows and 2 cols where each col stores x or y of the current open slot
open_slots = []


#for debugging
do_next = IntVar()
next_button = None

#for analysis
excel_list = []

#labels for ranges that have been secured by a player
secured_labels = []



def main():
    create_all_options()
    render()




def render():
    global rad_val
    global player_labels
    global next_button
    global open_slots


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

    D = tk.Button(root, text ="start")
    D.grid(row=12,column=13)
    D.config(command = starter)

    next_button = tk.Button(root, text ="next")
    print("assigned button was:")
    print(next_button)
    next_button.grid(row=12,column=15)
    next_button.config(command = lambda: do_next.set(1))
    print(next_button)

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
        result_arr.append("E")
        result_arr.append("O")
    else:
        p1_target = "odd"
        p2_target = "even"
        result_arr.append("O")
        result_arr.append("E")

    fill_inner(1)
    for i in value_matrix:

        print(i)

    score_labels[0] = tk.Label(root, text=0,
        borderwidth=0, height = 4, width = 5)
    score_labels[0].grid(row=4,column=13, columnspan = 2)

    score_labels[1] = tk.Label(root, text=0,
        borderwidth=0, height = 4, width = 5)
    score_labels[1].grid(row=6,column=13, columnspan = 2)

    p1 = tk.Label(root, text="Player 1 - %s" %(p1_target),
        borderwidth=0, height = 3, width = 15)
    p1.grid(row=3,column=13, columnspan = 2, rowspan = 2)
    player_labels[0]= p1

    p2 = tk.Label(root, text="Player 2 - %s" %(p2_target),
        borderwidth=0, height = 3, width = 15)
    p2.grid(row=5,column=13, columnspan = 2, rowspan = 2)
    player_labels[1] = p2

    player_labels[0].configure(font="sans 16 bold")
    player_labels[1].configure(font="sans 13")

    # render the options_remaining hor_labels
    o1 = tk.Label()

    freeze_allx()
    counter=0
    while(1==1):
        counter = counter+1
        open_slots = []

        unfreeze_range(2,10)
        unfreeze_range(1,10)
        if (check_loner_open()):
            break
    print("it took %d times to choose a board" % counter)

    open_buttons()

    show_inner()
    update_scores()
    for i in range(0,9):
        for j in range(0,9):
            change_sums(i,j)

    update_secured()


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
    print("we unfroze:")
    print(x)
    global open_slots

    #if want to unfreeze whole loop
    if (count == -1):

        for a in looper(x):
            button_matrix[a[0]][a[1]].configure( state = "normal")

    else:
        #if want to unfreeze specific cells within the ring
        arr = looper(x)
        print(looper(x))
        chosen = random.sample(arr, count)

        open_slots_now = []

        for a in chosen:

            #store the cells that were unfrozen for use by the auto-player
            open_slots_now.append(copy.deepcopy(a))
        print("opened slots:")
        print(open_slots)

    open_slots = copy.deepcopy(open_slots + open_slots_now)



def fix():
    a = root.winfo_geometry().split('+')[0]
    b = a.split('x')
    w = int(b[0])
    h = int(b[1])
    root.geometry('%dx%d' % (w+1,h+1))

def create_all_options():
    global option_matrix1
    global option_matrix2

    #total_options = [1,3,5,7,9,1,3,5,7,9]
    # # total_options = [1,3,5,7,9,11,13,15,17,19,21,23]
    # # total_options = [0,1,2,3,4,5,6,7,8,9,10,11]
    # # total_options = [0,2,4,6,8,10,12,14,16,18,20,22]
    total_options = [0,1,2,3,4,5,6,7,8,9]
    for i in range(0,total_rounds-2):
        for j in range(0,num_open//2):
            #print(total_options)

            chosen_curr = random.choice(total_options)
            total_options.remove(chosen_curr)
            option_matrix1[i][j] = chosen_curr
            #option_matrix2[i][j] = chosen_curr



    # option_matrix1[0][0] = 2
    # option_matrix1[0][1] = 2
    # option_matrix1[0][2] = 4
    # option_matrix1[0][3] = 6
    # option_matrix1[0][4] = 8
    #
    # option_matrix1[1][0] = 1
    # option_matrix1[1][1] = 3
    # option_matrix1[1][2] = 5
    # option_matrix1[1][3] = 7
    # option_matrix1[1][4] = 9



    option_matrix2 = copy.deepcopy(option_matrix1)



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
        radb.grid(row = i, column = 18)
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
    global next_button
    global excel_list
    print(next_button)
    #next_button.wait_variable(do_next)
    print(r)
    print(c)
    print(val)

    global rad_val
    rad_val.set(val)
    assert(rad_val.get() != -1), "rad_val was -1"
    global turn_count
    global ended
    turn_count = turn_count+1
    # if (turn_count//num_open >= total_rounds-2):
    #     ended=1
    #     print("endedxx")
    #     update_scores()
    #     freeze_all()

    global open_slots
    open_slots.remove([r,c])
    print ("open_slots:")
    print(open_slots)


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
    update_secured()
    update_scores()
    change_sums(r,c)

    #change text of button pressed
    b.config(text = rad_val.get(), font='sans 13 bold', state="disabled")
    root.update()
    print("printing val_matr:\n")
    print(value_matrix)
    #b.config(text = rad_val.get())
    change_sums(r,c)

    # based on current even and odd sum, decides and appends to the result_arr array (0->d, player-1->1, player-2->2)
    record_scores()
    if (turn_count//num_open >= total_rounds-2):
        ended=1
        print("endedxx")
        #update_scores()
        freeze_all()
    if (turn_count%2 == 0):
        #record_scores()
        print("recorded_scores:")
        print(result_arr)


    # else:
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


    if (turn_count%num_open == 0):

        display_new_round()

        rounds = rounds+1
        print("rounds changed to:")
        print(rounds)
        #change_board()


    #switch players after every turn
    if (curr_player == 1):
        print("predicted:")

        #if starting new round then repeat previous player and highlight appropriately
        if (turn_count%num_open == 0):
            curr_player = 2
            # player_labels[0].configure(font="sans 16 bold")
            # player_labels[1].configure(font="sans 13")
            #print(decide_move(1))
        else:
            #done in "else" since we change only if non-new round
            curr_player = 2
            #print(decide_move(2))
    else:
        print("predicted:")


        #if starting new round then repeat previous player and highlight appropriately
        if (turn_count%num_open == 0):
            curr_player = 1
            # player_labels[1].configure(font="sans 16 bold")
            # player_labels[0].configure(font="sans 13")
            #print(decide_move(2))
        else:
            #done in "else" since we change only if non-new round
            curr_player = 1
            #print(decide_move(1))




    global p1_target
    global p2_target

    #this following if elif else is for recording in excel_list
    if (curr_player == 1):
        if (p1_target == "even"):
            excel_list.append("E")
        elif (p1_target == "odd"):
            excel_list.append("O")
        else:
            assert(1==2),"the player target is non even and non odd - wrongly assigned"

    elif (curr_player == 2):
        if (p2_target == "even"):
            excel_list.append("E")
        elif (p2_target == "odd"):
            excel_list.append("O")
        else:
            assert(1==2),"the player target is non even and non odd - wrongly assigned"
    else:
        assert(1==2),"there was a non 1 or 2 curr_player value"

    if (auto_player == curr_player):
        # t0 = time.time()
        # for i in range(10000):
        #     auto_move = decide_move(auto_player)
        # t1 = time.time()
        #time.sleep(0)

        #total = t1-t0
        #print(total)

        #time.sleep(0.5)

        auto_move = decide_move(auto_player)
        print("it played:")
        print(auto_move)
        excel_list = excel_list +  get_pos_val_concat(auto_move)
        #change_value_matrix(auto_move[0],auto_move[1], auto_move[2], button_matrix[auto_move[0]][auto_move[1]])

    else:
        #time.sleep(0)
        #auto_move = decide_move(auto_player-1)
        auto_move = decide_move(curr_player)
        excel_list = excel_list +  get_pos_val_concat(auto_move)
        #change_value_matrix(auto_move[0],auto_move[1], auto_move[2], button_matrix[auto_move[0]][auto_move[1]])




def record_scores():
    global excel_list
    even_sum = get_even_odd_sums()[0]
    odd_sum = get_even_odd_sums()[1]

    excel_list.append(odd_sum)
    excel_list.append(even_sum)

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
    global excel_list


    if (turn_count//num_open >= total_rounds-2):

        freeze_all()
        resultarrstr = ""
        for i in result_arr:
            resultarrstr = resultarrstr + str(i) + "  "


        p1_wins = result_arr.count(1)
        p2_wins = result_arr.count(2)
        draw_count = result_arr.count(0)

        resultarrstr =  resultarrstr + "\n"
        resultarrstr =  resultarrstr + "P1-> " + str(p1_wins) + "\n"
        resultarrstr =  resultarrstr + "P2-> " + str(p2_wins) + "\n"

        resultarrstr =  resultarrstr + "Draw-> " + str(draw_count)

        file_append()

        showinfo("Information", resultarrstr)
        clearer()
        exit()


    #assigning correct round_starter player since each round alternates
    if (round_start_player == 2):
        round_start_player = 1
    else:
        round_start_player = 2

    curr_options = option_matrix1[turn_count//num_open]
    curr_options1 = option_matrix1[turn_count//num_open]
    curr_options2 = option_matrix2[turn_count//num_open]

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

    if (p1_target == "even"):
        score_labels[0].config(text = even_sum)
        score_labels[1].config(text = odd_sum)
    else:
        score_labels[0].config(text = odd_sum)
        score_labels[1].config(text = even_sum)

#returns an array which returns the sums of the even and odd col and row totals in an array [even_sum, odd_sum]
#for the global value-matrix
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
#for the global value-matrix
def row_sum(i):
    global value_matrix
    summed = sum(value_matrix[i])

    return summed

#calculates sum of given col
#for the global value-matrix
def col_sum(i):
    global value_matrix
    summed = sum(row[i] for row in value_matrix)

    return summed


#for the given matrix, not global
def get_even_odd_sums_given(matrix):
    global max_size
    even_sum = 0
    odd_sum = 0

    for i in range(max_size):
        curr_sum_vert = row_sum_given(i, matrix)
        if (curr_sum_vert%2 == 0):
            even_sum = even_sum+curr_sum_vert
        else:
            odd_sum = odd_sum+curr_sum_vert

        curr_sum_hor = col_sum_given(i, matrix)
        if (curr_sum_hor%2 == 0):
            even_sum = even_sum+curr_sum_hor
        else:
            odd_sum = odd_sum+curr_sum_hor

    return [even_sum, odd_sum]

#calculates sum of given row
#for the given matrix, not global
def row_sum_given(i, matrix):

    summed = sum(matrix[i])

    return summed

#calculates sum of given col
#for the given matrix, not global
def col_sum_given(i, matrix):

    summed = sum(row[i] for row in matrix)

    return summed


def change_board():
    global rounds
    global total_rounds
    freeze_all()
    unfreeze_range(total_rounds-rounds, 10)


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

def starter():
    global auto_player
    global excel_list
    global p1_target

    auto_move = []

    if (p1_target == "even"):
        excel_list.append("E")
        print("appended")
    elif (p1_target == "odd"):
        excel_list.append("O")
        print("appended")
    else:
        assert(1==2),"the player target is non even and non odd - wrongly assigned"

    if (auto_player == 1):
        auto_move = decide_move(1)
    elif(auto_player == 2):
        auto_move = decide_move(1)
    else:
        assert(1==2), "the auto-player number was not 1 or 2 but something else"
    assert (auto_move != []), "no move-1 was created"

    excel_list = excel_list +  get_pos_val_concat(auto_move)

    change_value_matrix(auto_move[0],auto_move[1], auto_move[2], button_matrix[auto_move[0]][auto_move[1]])
    root.update_idletasks()

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

# decides the move for the auto player based on whether it is 1 or 2 (val of parameter player is 1 or 2)
def decide_move(player):
    global p1_target
    global p2_target
    global curr_options1
    global curr_options2
    global value_matrix
    global open_slots

    usable_options = []
    given_matrix = copy.deepcopy(value_matrix)


    chase = ""
    if (player == 1):
        chase = p1_target
        usable_options = curr_options1


    if (player == 2):
        chase = p2_target
        usable_options = curr_options2

    #creating a dict to store [difference, action]
    #for multiple actions where action is [row,col,used_option]
    action_result = {}
    #loop through the options and see which one gives the best best result
    #the position comes from the slots that are currently opened#this is (0)n^2
    for insertion in usable_options:
        for position in open_slots:
            initial_val = given_matrix[position[0]][position[1]]

            #make sure that you are trying to test changing something that is 0 since all empties/unentered are 0
            assert(initial_val == 0)

            given_matrix[position[0]][position[1]] = insertion

            #use get_even_odd_sums_given to get the even and odd sums after the current change made
            even_odd_sums_arr = get_even_odd_sums_given(given_matrix)
            diff_ev_minus_odd = even_odd_sums_arr[0] - even_odd_sums_arr[1]

            #store this result in the dict action_result
            action_result[diff_ev_minus_odd] = [position[0], position[1], insertion]

            #reverse the change and move to the next options
            given_matrix[position[0]][position[1]] = initial_val

    #if I am chasing even then I want even-odd scores to be max
    if (chase == "even"):
        differences = action_result.keys()
        max_diff = max(differences)

        return action_result[max_diff]


    #if I am chasing even then I want even-odd scores to be max
    if (chase == "odd"):
        differences = action_result.keys()
        min_diff = min(differences)

        return action_result[min_diff]

    #should never reach here
    assert(1==2)
    return -1


# decides the move for the auto player based on whether it is 1 or 2 (val of parameter player is 1 or 2)
def decide_random(player):
    global p1_target
    global p2_target
    global curr_options1
    global curr_options2
    global value_matrix
    global open_slots

    usable_options = []
    given_matrix = copy.deepcopy(value_matrix)

    if (player == 1):
        usable_options = curr_options1


    if (player == 2):
        usable_options = curr_options2

    rand_pos = random.choice(open_slots)
    rand_val = random.choice(usable_options)

    return [rand_pos[0],rand_pos[1],rand_val]



    #should never reach here
    assert(1==2)
    return -1

def next_true():
    do_next = 1


def fill_inner(val):
    global value_matrix
    global excel_list
    global p1_target
    global p2_target

    p1_letter = ""
    p2_letter = ""
    if (p1_target == "even"):
        p1_letter = "E"
        p2_letter = "O"
    elif (p1_target == "odd"):
        p1_letter = "O"
        p2_letter = "E"
    else:
        assert (1==2), "player target is not even or odd"


    value_matrix[3][4] = val
    excel_list.append(p1_letter)
    excel_list = excel_list + get_pos_val_concat([3,4,val])
    record_scores()

    value_matrix[5][4] = val
    excel_list.append(p2_letter)
    excel_list = excel_list + get_pos_val_concat([5,4,val])
    record_scores()

    value_matrix[4][3] = val
    excel_list.append(p1_letter)
    excel_list = excel_list + get_pos_val_concat([4,3,val])
    record_scores()

    value_matrix[4][5] = val
    excel_list.append(p2_letter)
    excel_list = excel_list + get_pos_val_concat([4,5,val])
    record_scores()

    #update_scores()

def show_inner():
    global value_matrix
    global button_matrix
    to_show = looper(3)
    print("ts is:")
    print(to_show)

    #show all those cells that are non-zero in the first ring
    for cell in to_show:
        if (value_matrix[cell[0]][cell[1]] != 0):
            button_matrix[cell[0]][cell[1]].configure(font='sans 13 bold', state="disabled", text = value_matrix[cell[0]][cell[1]])


def get_pos_val_concat(pos_val_arr):
    row = pos_val_arr[0]
    col = pos_val_arr[1]
    val = pos_val_arr[2]

    row_visual = row+1
    col_visual = 'Z'
    ascii_col = 65+col
    col_char = chr(ascii_col)
    return [str(col_char) + str(row_visual),val]


def check_loner_open():
    global open_slots

    rows_filled = [row[0] for row in open_slots]
    cols_filled = [row[1] for row in open_slots]

    satisfies = True

    for elem in rows_filled:
        if (rows_filled.count(elem) == 1):
            satisfies = False
            return False

    for elem in cols_filled:
        if (cols_filled.count(elem) == 1):
            satisfies = False
            return False

    return True


def update_secured():
    global value_matrix
    global secured_labels
    global open_slots
    global root

    open_rows = []
    open_cols = []

    for slot in open_slots:
        if (slot[0] not in open_rows):
            open_rows.append(copy.deepcopy(slot[0]))

        if (slot[1] not in open_cols):
            open_cols.append(copy.deepcopy(slot[1]))
    print("open cols then rows:")
    print(open_cols)
    print(open_rows)

    even_secured = 0
    odd_secured = 0

    for rc in range(0,8):
        if (rc not in open_rows):
            curr_row_sum = row_sum(rc)
            if (curr_row_sum%2 == 0):
                even_secured = even_secured + curr_row_sum
            else:
                odd_secured = odd_secured + curr_row_sum

        if (rc not in open_cols):
            curr_col_sum = col_sum(rc)
            if (curr_col_sum%2 == 0):
                even_secured = even_secured + curr_col_sum
            else:
                odd_secured = odd_secured + curr_col_sum

    if (secured_labels == []):
        #even label
        sec_even = tk.Label(root, text="even - %d" %(even_secured),
            borderwidth=0, height = 3, width = 15)
        sec_even.grid(row=0,column=13, columnspan = 2, rowspan = 1)
        secured_labels.append(sec_even)


        #odd_label
        sec_odd = tk.Label(root, text="odd - %d" %(odd_secured),
            borderwidth=0, height = 3, width = 15)
        sec_odd.grid(row=1,column=13, columnspan = 2, rowspan = 1)
        secured_labels.append(sec_odd)

    else:
        #if the list is already populated, only configure the text in the labels that already exist
        secured_labels[0].configure(text="even - %d" %(even_secured))
        secured_labels[1].configure(text="odd - %d" %(odd_secured))



def open_buttons():
    #unfreeze the relevant buttons
    global button_matrix
    global value_matrix
    for a in open_slots:
        button_matrix[a[0]][a[1]].configure( state = "normal", text = value_matrix[a[0]][a[1]])

def file_append():
    global result_arr
    global excel_list

    joined = ",".join(str(x) for x in result_arr)
    joined_details = ",".join(str(x) for x in excel_list)
    with open("output.txt", "a") as myfile:
        myfile.write(joined)
        myfile.write(","+joined_details+"\n")
    #print(result_arr)
    return


def clearer():
    global num_ope

    #stays the same
    global total_round


    global value_matrix
    global button_matrix
    global option_matrix1
    global option_matrix2
    global radio_list
    global root
    global rad_val
    global turn_count
    #curr_options = option_matrix[0]
    global curr_options1
    global curr_options2
    global curr_player
    global vert_labels
    global hor_labels
    global p1_score
    global p1_target
    global p2_score
    global p2_target
    global score_labels
    global max_size


    global rounds
    global round_start_player
    global player_labels
    global ended

    global auto_player


    # number of rounds out of the 12 that are counted
    global countable_rounds

    # 1 for player 1, 2 for player 2 , 0 for draw when filled
    global result_arr

    # player option label radio_list
    global p_opt_labels

    # stores currently open buttons (array of x,y) pair arrays
    # has num_open rows and 2 cols where each col stores x or y of the current open slot
    global open_slots


    #for debugging
    global do_next
    global next_button

    #for analysis
    global excel_list

    global num_ope

    #stays the same
    global total_round









    del value_matrix
    del button_matrix
    del option_matrix1
    del option_matrix2
    del radio_list
    del root
    del rad_val
    del turn_count
    #curr_options = option_matrix[0]
    del curr_options1
    del curr_options2
    del curr_player
    del vert_labels
    del hor_labels
    del p1_score
    del p1_target
    del p2_score
    del p2_target
    del score_labels
    del max_size


    del rounds
    del round_start_player
    del player_labels
    del ended

    del auto_player


    # number of rounds out of the 12 that are counted
    del countable_rounds

    # 1 for player 1, 2 for player 2 , 0 for draw when filled
    del result_arr

    # player option label radio_list
    del p_opt_labels

    # stores currently open buttons (array of x,y) pair arrays
    # has num_open rows and 2 cols where each col stores x or y of the current open slot
    del open_slots


    #for debugging
    del do_next
    del next_button

    #for analysis
    del excel_list












if __name__ == "__main__":
    main()
