from gamestate import Gamestate
from myboard import Myboard

# Used to run all the code
if __name__ == '__main__':
    # Creates a board with given parameters
    board = Myboard(20, 20, 75)
    # Adds mines into the board
    board.add_mines()
    # Creates a game from the given board
    game = Gamestate(board.make_tiles(), board.safespots())
    # Draws and begins the game
    game.draw()
