import curses
import curses.ascii
from position import Position
from piece import Color
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
    b.position = Position.base()
    b.position.move_san("Nc3", Color.WHITE)
    b.play()

curses.wrapper(main)
