from utils import randcell
import os


class Helicopter:

    def __init__(self, width, height):
        start_point = randcell(width, height)
        start_point_x = start_point[0]
        start_point_y = start_point[1]
        self.x = start_point_x
        self.y = start_point_y
        self.width = width
        self.height = height
        self.maxtank = 1
        self.tank = 0
        self.score = 0
        self.lives = 20

    def move(self, helic_x, helic_y):
        new_helic_x = helic_x + self.x
        new_helic_y = helic_y + self.y
        if (new_helic_x >= 0) and (new_helic_x < self.height) and (new_helic_y >= 0) and (new_helic_y < self.width):
            self.x = new_helic_x
            self.y = new_helic_y

    def print_stats(self):
        global new_map
        print("🛢 ", self.tank, "/", self.maxtank, sep="", end=" | ")
        print("🏆", self.score, end=" | ")
        print("🧡", self.lives)

    def game_over(self, operation_system, listener):
        os.system(operation_system)
        print("=================================")
        print("")
        print(" GAME OVER, YOUR SCORE IS", self.score)
        print("")
        print("=================================")
        listener.stop()
        exit(0)

    def export_data(self):
        return {"score": self.score,
                "lives": self.lives,
                "x": self.x, "y": self.y,
                "tank": self.tank, "maxtank": self.maxtank}

    def import_data(self, data):
        self.x = data["x"] or 0
        self.y = data["y"] or 0
        self.tank = data["tank"] or 0
        self.maxtank = data["maxtank"] or 1
        self.lives = data["lives"] or 3
        self.score = data["score"] or 0
