import curses
import curses.ascii
from position import Position
from board import Board
from pgn_parser import pgn, parser
import time

def main(w):
    # Clear screen
    w.clear()
    curses.curs_set(0)
    curses.start_color()

    # Define colors pairs
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_WHITE)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_BLACK, curses.COLOR_BLACK)
    curses.init_pair(6, curses.COLOR_RED, curses.COLOR_WHITE)
    
    # Create a new board
    b = Board(w)

    # Set the board's position to be the base position
    b.position = Position.base()
    b.position.move("e2", "e4")
    b.position.move("e7", "e5")
    b.position.move("g1", "f3")
    b.position.move("b8", "c6")
    b.position.move("d2", "d4")
    
    b.play()

curses.wrapper(main)
