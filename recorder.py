import game_condensed_firstrandom_no_UI
import time
import importlib




start = time.time()

for i in range (1000):

    importlib.reload(game_condensed_firstrandom_no_UI)
    game_condensed_firstrandom_no_UI.main()

end = time.time()

print("time was:")
print(end - start)
