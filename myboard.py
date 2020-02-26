import random
from math import floor
from pip._vendor.msgpack.fallback import xrange
from tile import Tile

# Class used to create a minesweeper board's backend, and converts into tiles to be used to create the UI
class Myboard:
    def __init__(self, width, height, numbombs):
        self.width = width
        self.height = height
        self.numbombs = numbombs
        self.game = []
        for x in range(width):
            currentrow = []
            for y in range(height):
                currentrow.append(0)
            self.game.append(currentrow)

    # Randomly adds mines into the 2D array of positions
    def add_mines(self):
        bombs = random.sample(xrange(self.height*self.width), self.numbombs)
        for location in bombs:
            x = floor(location / self.height)
            y = location % self.height
            self.adjustnums(x, y)
            self.game[x][y] = -1

    # Adjusts all the numbers around the given mine to be one greater
    def adjustnums(self, x, y):
        self.increase_num(x - 1, y)
        self.increase_num(x - 1, y - 1)
        self.increase_num(x - 1, y + 1)
        self.increase_num(x + 1, y)
        self.increase_num(x + 1, y - 1)
        self.increase_num(x + 1, y + 1)
        self.increase_num(x, y - 1)
        self.increase_num(x, y + 1)

    # Increments the value at the given coordinate if not a bomb or an invalid coord
    def increase_num(self, x, y):
        if 0 <= x < self.width and 0 <= y < self.height:
            if self.game[x][y] != -1:
                self.game[x][y] = self.game[x][y] + 1

    # Creates a 2d array of tiles representing the board generated in the constructor
    def make_tiles(self):
        all_tiles = []
        for row in range(self.width):
            current_row = []
            for col in range(self.height):
                cur_tile = Tile(row, col, self.game[row][col])
                current_row.append(cur_tile)
            all_tiles.append(current_row)
        return all_tiles

    # Calculates the total number of non bomb spots
    def safespots(self):
        return (self.height*self.width)-self.numbombs
