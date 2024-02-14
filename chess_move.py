from piece import Piece

class ChessMove:
    def __init__(self, piece, start, end, captured_piece=Piece.No_Piece):
        self.piece = piece
        self.start = start
        self.end = end
        self.captured_piece = captured_piece

    def __str__(self):
        return f"Move {self.piece} from {self.start} to {self.end}"

    def __repr__(self):
        return f"Move {self.piece} from {self.start} to {self.end}"