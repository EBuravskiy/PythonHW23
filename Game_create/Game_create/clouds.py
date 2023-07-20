from utils import randbool


class Clouds:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.cells = [[0 for i in range(width)] for j in range(height)]
        self.x = self.cells[0]
        self.y = self.cells[1]

    def update(self, rand=1, maxrand=20, grand=1, maxgrand=10):
        for i in range(self.height):
            for j in range(self.width):
                if randbool(rand, maxrand):
                    self.cells[i][j] = 1
                    if randbool(grand, maxgrand):
                        self.cells[i][j] = 2
                else:
                    self.cells[i][j] = 0

    def export_data(self):
        return {"cells": self.cells}

    def import_data(self, data):
        self.cells = data["cells"] or [
            [0 for i in range(self.width)] for j in range(self.height)]
