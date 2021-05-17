from piece import Piece, PieceType, Color
from enum import Enum, auto
    
class MoveResult(Enum):
    SUCCESS = auto()

# A class representing a chess board
class Position(dict):
    def base() -> "Position":
        # Create a dictionary to map positions to pieces
        board = {}

        # The layout of the pieces on the first and eigth row
        layout = [
            PieceType.ROOK,
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
        return Position(board)
    
    # Moves a piece in the position. This does not check to see
    # if the move is valid. It also overrites whatever is in
    # square_to (the square the piece is being moved to) and
    # erasing the piece in square_from (the square the piece is
    # being moved from)
    def raw_move(self, square_from: str, square_to: str):
        self[square_to] = self[square_from]
        self[square_from] = {}
    
    def validate_move(
            self, 
            square_from: str, 
            square_to: str
    ) -> MoveResult:
        return MoveResult.SUCCESS
    
    def move(self, square_from: str, square_to: str) -> MoveResult:
        result = validate_move(square_from, square_to)
        if result.name == MoveResult.SUCCESS: move_piece
        return result
