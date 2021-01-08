import game_condensed_firstrandom_no_UI
import time
import importlib
# import tkinter as tk
# from tkinter import *
# from tkinter.messagebox import showinfo
#
# import random
# import copy
# import time




start = time.time()

for i in range (100):

    importlib.reload(game_condensed_firstrandom_no_UI)
    game_condensed_firstrandom_no_UI.main()
    if (i%99 == 0):
        print(time.time() - start)
        start = time.time()

# end = time.time()

# print("time was:")
# print(end - start)
