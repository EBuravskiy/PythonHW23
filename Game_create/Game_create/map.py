from random import randint
from utils import randcell
from utils import randnearcell


CELL_TYPES = "🟩🌲🟦🏥🏭🔥"
TREE_BONUS = 100
UPGRADE_COST = 5000
LIFE_COST = 10000


class Map(object):

    def __init__(self, width, heigth):
        self.width = width
        self.height = heigth
        self.cells = [[0 for i in range(self.width)]
                      for j in range(self.height)]
        for i in range(width * heigth // 100):
            self.generate_forest(width * heigth // 100 * 40)
        for i in range(width * heigth // 200):
            self.generate_rivers(width)
        self.generate_upgrade_shop()
        self.generate_hospital()

    def check_bounds(self, x, y):
        if (x < 0) or (y < 0) or (x >= self.height) or (y >= self.width):
            return False
        return True

    def created_map(self, helicopter, clouds):
        print("⬛" * (self.width + 2))
        for map_row in range(self.height):
            print("⬛", end="")
            for map_cols in range(self.width):
                cell = self.cells[map_row][map_cols]
                if (clouds.cells[map_row][map_cols] == 1):
                    print("☁︎ ", end="")
                elif (clouds.cells[map_row][map_cols] == 2):
                    print("🌪️ ", end="")
                elif (helicopter.x == map_row and helicopter.y == map_cols):
                    print("🚁", end="")
                # проверка на выход за пределы строки содержащей картинки
                elif (cell >= 0) and (cell < len(CELL_TYPES)):
                    print(CELL_TYPES[cell], end="")
            print("⬛")
        print("⬛" * (self.width + 2))

    def generate_forest(self, long):
        rand_cell = randcell(self.width, self.height)
        rand_x = rand_cell[0]
        rand_y = rand_cell[1]
        self.cells[rand_x][rand_y] = 1
        while long > 0:
            rand_near_cell = randnearcell(rand_x, rand_y)
            rand_near_cell_x = rand_near_cell[0]
            rand_near_cell_y = rand_near_cell[1]
            if self.check_bounds(rand_near_cell_x, rand_near_cell_y) and (self.cells[rand_near_cell_x][rand_near_cell_y] == 0) and (self.cells[rand_near_cell_x][rand_near_cell_y] != 1):
                self.cells[rand_near_cell_x][rand_near_cell_y] = 1
                rand_x = rand_near_cell_x
                rand_y = rand_near_cell_y
                long -= 1
            else:
                long -= 1

    def generate_tree(self):
        new_tree = randcell(self.width, self.height)
        new_tree_x = new_tree[0]
        new_tree_y = new_tree[1]
        if (self.check_bounds(new_tree_x, new_tree_y) and self.cells[new_tree_x][new_tree_y] == 0):
            self.cells[new_tree_x][new_tree_y] = 1
        else:
            self.generate_tree()

    def generate_rivers(self, long):
        rand_cell = randcell(self.width, self.height)
        rand_x = rand_cell[0]
        rand_y = rand_cell[1]
        self.cells[rand_x][rand_y] = 2
        while long > 0:
            rand_near_cell = randnearcell(rand_x, rand_y)
            rand_near_cell_x = rand_near_cell[0]
            rand_near_cell_y = rand_near_cell[1]
            if self.check_bounds(rand_near_cell_x, rand_near_cell_y) and (self.cells[rand_near_cell_x][rand_near_cell_y] != 2):
                self.cells[rand_near_cell_x][rand_near_cell_y] = 2
                rand_x = rand_near_cell_x
                rand_y = rand_near_cell_y
                long -= 1
            else:
                long -= 1

    def generate_upgrade_shop(self):
        shop_cell = randcell(self.width, self.height)
        shop_x = shop_cell[0]
        shop_y = shop_cell[1]
        self.cells[shop_x][shop_y] = 4

    def generate_hospital(self):
        hospital_cell = randcell(self.width, self.height)
        hospital_x = hospital_cell[0]
        hospital_y = hospital_cell[1]
        if self.cells[hospital_x][hospital_y] == 0:
            self.cells[hospital_x][hospital_y] = 3
        else:
            self.generate_hospital()

    def add_fire(self):
        fire = randcell(self.width, self.height)
        fire_x = fire[0]
        fire_y = fire[1]
        if (self.cells[fire_x][fire_y] == 1):
            self.cells[fire_x][fire_y] = 5
        else:
            self.add_fire()

    def update_fire(self, helicopter, operation_system, listener):
        for fire_cell_x in range(self.height):
            for fire_cell_y in range(self.width):
                if self.cells[fire_cell_x][fire_cell_y] == 5:
                    self.cells[fire_cell_x][fire_cell_y] = 0
                    if self.cells[fire_cell_x][fire_cell_y] == 0:
                        helicopter.score -= TREE_BONUS
                        if helicopter.score < 0:
                            helicopter.game_over(operation_system, listener)
                    rand_near_cell = randnearcell(fire_cell_x, fire_cell_y)
                    rand_near_cell_x = rand_near_cell[0]
                    rand_near_cell_y = rand_near_cell[1]
                    if self.check_bounds(rand_near_cell_x, rand_near_cell_y) and (self.cells[rand_near_cell_x][rand_near_cell_y] == 1):
                        self.cells[rand_near_cell_x][rand_near_cell_y] = 5
        for i in range(randint(0, 3)):
            self.add_fire()

    def process_helicopter(self, helicopter, clouds, operation_system, listener):
        helicopter_coordinates = self.cells[helicopter.x][helicopter.y]
        ligthing_coordinates = clouds.cells[helicopter.x][helicopter.y]
        if (helicopter_coordinates == 2):
            helicopter.tank = helicopter.maxtank
        if ((helicopter_coordinates == 5) and (helicopter.tank > 0)):
            helicopter.tank -= 1
            helicopter.score += TREE_BONUS
            self.cells[helicopter.x][helicopter.y] = 1
        if (helicopter_coordinates == 4 and helicopter.score >= UPGRADE_COST):
            helicopter.score -= UPGRADE_COST
            helicopter.maxtank += 1
        if (helicopter_coordinates == 3 and helicopter.score >= LIFE_COST):
            helicopter.score -= LIFE_COST
            helicopter.lives += 1000
        if (ligthing_coordinates == 2):
            helicopter.lives -= 1
            if helicopter.lives == 0:
                helicopter.game_over(operation_system, listener)

    def export_data(self):
        return {"cells": self.cells}

    def import_data(self, data):
        self.cells = data["cells"] or [[0 for i in range(self.width)]
                                       for j in range(self.height)]
