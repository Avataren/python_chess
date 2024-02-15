from piece import Piece

class ChessMove:
    def __init__(self, piece:Piece, start, end, captured_piece=Piece.No_Piece, captured_position=None):
        self.piece = piece
        self.start = start
        self.end = end
        self.captured_piece = captured_piece
        self.captured_position = captured_position if captured_position else end

    def __str__(self):
        return f"ChessMove {self.piece} from {self.start} to {self.end}, captured: {self.captured_piece} at {self.captured_position}"

    def __repr__(self):
        return f"ChessMove {self.piece} from {self.start} to {self.end}, captured: {self.captured_piece} at {self.captured_position}"