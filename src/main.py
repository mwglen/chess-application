import curses
from enum import Enum, auto

def main(w):
    # Clear screen
    w.clear()
    curses.curs_set(0)
    curses.start_color()

    # Define colors pairs
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_BLACK)

    # Color the main window
    w.bkgd(" ", curses.color_pair(1))
    w.box("|", "-")

    # Add the title
    w.addstr(0, 0, "Chess Application", curses.color_pair(1))
   
    # Build and draw the board
    board = Board(w)
    board.draw()
   
    # Wait for keypress
    w.getch()

# A class representing a chess board
class Position(dict):
    def base() -> dict:
        # Create a dictionary to map positions to pieces
        board = {}

        # The layout of the pieces on the first and eigth row
        layout = [
            PieceType.PAWN,
            PieceType.KNIGHT,
            PieceType.BISHOP,
            PieceType.QUEEN,
            PieceType.KING,
            PieceType.BISHOP,
            PieceType.KNIGHT,
            PieceType.ROOK,
        ]

        # Position the pieces on the board
        for (col, pt) in zip("abcdefgh", layout):
            # Position the pawns
            for (row, c) in zip("27", Color):
                board[col + row] = Piece(PieceType.PAWN, c)
            # Position the other pieces
            for (row, c) in zip("18", Color):
                board[col + row] = Piece(pt, c)

        # Return the dictionary
        return board

class Board():
    # Creates a board without any pieces on it
    def __init__(self, base_window):
        # Use a position with no pieces in it
        self.position = Position.base()
        
        windows = {}
        height = 3
        width = 6
        y = 10
        x = 10
        for row in "12345678":
            for col in "abcdefgh":
                w = base_window.subwin(height, width, y, x)
                w.bkgd(row)
                windows[col + row] = w
                x += width
            y += height
            x = 10
        self.windows = windows

    def draw(self):
        for (i, col) in enumerate("abcdefgh"):
            for row in "12345678":
                # Get the window corresponding to this square
                w = self.windows[col + row]
                
                # Color the Square
                if (int(row) % 2 == 0) ^ (i % 2 == 0):
                    w.bkgd(" ", curses.color_pair(1)) # Color White
                else:
                    w.bkgd(" ", curses.color_pair(2)) # Color Black

                # Get the peice at this square
                piece = self.position.get(col + row)
                
                # Draw the piece if needed
                if piece:
                    w.addch(0, 0, piece.type.as_letter())

# Types of pieces
class PieceType(Enum):
    PAWN = auto()
    KNIGHT = auto()
    BISHOP = auto()
    ROOK = auto()
    QUEEN = auto()
    KING = auto()

    # Returns the letter corresponding to the piece type
    def as_letter(self) -> str:
        if self.name == "PAWN":
            return 'P'
        elif self.name == "KNIGHT":
            return 'N'
        elif self.name == "BISHOP":
            return 'B'
        elif self.name == "ROOK":
            return 'R'
        elif self.name == "QUEEN":
            return 'Q'
        elif self.name == "KING":
            return 'K'

# Possible colors for a piece
class Color(Enum):
    WHITE = auto()
    BLACK = auto()

# A piece with a specified color
class Piece:
    def __init__(self, pt: PieceType, c: Color):
        self.type = pt
        self.color = c

curses.wrapper(main)
