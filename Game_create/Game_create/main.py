from pynput import keyboard
from map import Map
import time
import os
import json
from helicopter import Helicopter
from clouds import Clouds
from utils import introduce
from utils import mapsize


TICK_SLIP = 0.05
TREE_ADD = 400
CLOUDS_UPDATE = 200
FIRE_UPDATE = 150

tick = 1

operation_system = "cls"
introduce()

map_width = 20
map_height = 10
# map_size = mapsize()
# map_width = map_size[0]
# map_height = map_size[1]

new_map = Map(map_width, map_height)
clouds = Clouds(map_width, map_height)
helicopter = Helicopter(map_width, map_height)

# pynput
MOVE_HELICOPTER = {'w': (-1, 0), 'd': (0, 1), 's': (1, 0), 'a': (0, -1)}


def on_release(key):
    global helicopter, tick, clouds, new_map
    c = key.char.lower()
    # обработка движений вертолета
    if c in MOVE_HELICOPTER.keys():
        move_x = MOVE_HELICOPTER[c][0]
        move_y = MOVE_HELICOPTER[c][1]
        helicopter.move(move_x, move_y)
    # сохранение игры
    elif c == 'f':
        data = {"helicopter": helicopter.export_data(),
                "clouds": clouds.export_data(),
                "map": new_map.export_data(),
                "tick": tick}
        with open("level.json", "w") as lvl:
            json.dump(data, lvl)
    # загрузка игры
    elif c == 'g':
        with open("level.json", "r") as lvl:
            data = json.load(lvl)
            tick = data["tick"] or 1
            helicopter.import_data(data["helicopter"])
            new_map.import_data(data["map"])
            clouds.import_data(data["clouds"])


listener = keyboard.Listener(on_release=on_release)
listener.start()

while True:
    os.system(operation_system)
    new_map.process_helicopter(helicopter, clouds, operation_system, listener)
    helicopter.print_stats()
    new_map.created_map(helicopter, clouds)
#    print("TICK", tick)
    tick += 1
    time.sleep(TICK_SLIP)
    if (tick % TREE_ADD == 0):
        new_map.generate_tree()
    if (tick % FIRE_UPDATE == 0):
        new_map.update_fire(helicopter, operation_system, listener)
    if (tick % CLOUDS_UPDATE == 0):
        clouds.update()
