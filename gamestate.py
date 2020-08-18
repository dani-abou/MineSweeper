import os
from math import floor
from tkinter import *


# Tracks the current state of the game, and updates according to user interactions
def restart():
    os.execl(sys.executable, sys.executable, *sys.argv)


class Gamestate:
    def __init__(self, tiles, safety):
        self.finished = False
        self.tiles = tiles
        self.safety = safety
        self.openspots = 0
        self.bombs = len(self.tiles) * len(self.tiles[0]) - self.safety

        # Instantiates the window
        self.master = Tk()
        self.master.winfo_toplevel().title("Minesweeper!!!")

        # Instantiates the clickable window
        self.canvas = Canvas(self.master, width=len(self.tiles) * 20, height=len(self.tiles[0]) * 20 + 30)
        self.canvas.bind("<Button-1>", self.open)
        self.canvas.bind("<Button-3>", self.flag)

        # Instantiates the restart button
        button1 = Button(self.master, text="Restart", command=restart, bg="lightblue")
        button1.configure(width=10, activebackground="#33B5E5", relief=FLAT)
        self.canvas.create_window(10, len(self.tiles[0]) * 20.1, anchor=NW, window=button1)

        # Instantiates the bomb counter
        self.bottom_text = Label(self.master, text="Bombs left:   " + str(self.bombs))
        self.canvas.create_window(200, len(self.tiles[0]) * 20.1, anchor=NW, window=self.bottom_text)

    # Draws the whole board
    def draw(self):
        for row in self.tiles:
            for tile in row:
                tile.drawtile(self.canvas)
        self.canvas.pack()
        mainloop()


    # Occurs on a left click and opens the tile, ends the game if needed
    # Converts the click's coordinates for the method that actually does the opening
    def open(self, event):
        if not self.finished:
            self.flood_open(floor(event.x / 20), floor(event.y / 20))
            self.game_won()

    # Occurs on a right click; checks if box is flagged or not, if is flagged unflags it, and visversa
    # Updates the bomb counter
    def flag(self, event):
        if not self.finished:
            current_tile = self.tiles[floor(event.x / 20)][floor(event.y / 20)]
            if current_tile.state == 0:
                current_tile.flag_tile(self.canvas)
                self.bombs = self.bombs - 1
            elif current_tile.state == 1:
                current_tile.unflag_tile(self.canvas)
                self.bombs = self.bombs + 1
            self.bottom_text.config(text="Bombs left:" + str(self.bombs))

    # Opens the tile at the given coords, uses recursion to flood if the tile is zero
    def flood_open(self, starting_x, starting_y):
        if 0 <= starting_x < len(self.tiles) and 0 <= starting_y < len(self.tiles[0]):
            self.adjustcounter(self.tiles[starting_x][starting_y])
            value = self.tiles[starting_x][starting_y].open_tile(self.canvas)
            if value == 0:
                self.flood_open(starting_x - 1, starting_y - 1)
                self.flood_open(starting_x - 1, starting_y)
                self.flood_open(starting_x - 1, starting_y + 1)
                self.flood_open(starting_x + 1, starting_y - 1)
                self.flood_open(starting_x + 1, starting_y)
                self.flood_open(starting_x + 1, starting_y + 1)
                self.flood_open(starting_x, starting_y + 1)
                self.flood_open(starting_x, starting_y - 1)
            if value == -1:
                self.game_over()

    # Transitions to the game over screen
    def game_over(self):
        self.finished = True
        self.canvas.create_text(self.canvas.winfo_width() / 2, self.canvas.winfo_height() / 2, text="Game Over!",
                                fill="blue", font=("Purisa", int(self.canvas.winfo_width() / 9)))

    # Transitions to the game won screen
    def game_won(self):
        if self.safety == self.openspots:
            self.finished = True
            self.canvas.create_text(int(self.canvas.winfo_width() / 2), int(self.canvas.winfo_height() / 2),
                                    text="You Win!", fill="blue", font=("Purisa", int(self.canvas.winfo_width() / 7)))

    # Used to update the stored number of open tiles only when needed
    def adjustcounter(self, tile):
        if tile.state != 2:
            self.openspots = self.openspots + 1
