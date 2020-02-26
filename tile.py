# A tile represents an individual square in the minesweeper board
from random import *


def tile_color():
    red = hex(choice(range(0, 255)))
    blue = hex(choice(range(0, 255)))
    green = hex(choice(range(0, 255)))
    return "#" + red[2:3] + blue[2:3] + green[2:3]


class Tile:
    def __init__(self, row, col, value):
        self.row = row
        self.col = col
        self.value = value
        self.state = 0

    # Draws a green square at the corresponding coordinates to represent an unopened tile
    def drawtile(self, canvas):
        canvas.create_rectangle(self.row * 20, self.col * 20, (self.row + 1) * 20, (self.col + 1) * 20, fill=tile_color())

    # Determines what color a number should be; purely preference
    def num_color(self):
        if self.value == 1:
            return "darkblue"
        elif self.value == 2:
            return "green"
        elif self.value == 3:
            return "red"
        elif self.value == 4:
            return "purple"
        elif self.value == 5:
            return "cyan"
        else:
            return "black"

    # Replaces the green square with a representation of an open square: a blank square if the value is 0,
    # a blank square with the value if the value is greater than 0, or a red square if the tile is a minem,
    # and updates the tile's status accordingly
    def open_tile(self, canvas):
        if self.state == 0:
            self.state = 2
            if self.value == -1:
                canvas.create_rectangle(self.row * 20, self.col * 20, (self.row + 1) * 20, (self.col + 1) * 20,
                                        fill="red")
            elif self.value == 0:
                canvas.create_rectangle(self.row * 20, self.col * 20, (self.row + 1) * 20, (self.col + 1) * 20,
                                        outline="black", fill="white")
            else:
                canvas.create_rectangle(self.row * 20, self.col * 20, (self.row + 1) * 20, (self.col + 1) * 20,
                                        outline="black", fill="white")
                canvas.create_text((self.row * 20) + 10, (self.col * 20) + 10, text=self.value, fill=self.num_color())
            return self.value

    # Replaces a green square with a yellow square representing a flagged tile and updates the tile's status
    def flag_tile(self, canvas):
        self.state = 1
        canvas.create_rectangle(self.row * 20, self.col * 20, (self.row + 1) * 20, (self.col + 1) * 20, fill="yellow")

    # Replaces a yellow square with a green square representing a standard unopened tile, and updates the tile's status
    def unflag_tile(self, canvas):
        self.state = 0
        canvas.create_rectangle(self.row * 20, self.col * 20, (self.row + 1) * 20, (self.col + 1) * 20, fill="green")
