from piece import Piece

class ChessMove:
    is_castling_move = False
    is_en_passant = False
    def __init__(self, piece:Piece, start, end, captured_piece=Piece.No_Piece, captured_position=None):
        self.piece = piece
        self.start = start
        self.end = end
        self.captured_piece = captured_piece
        self.captured_position = captured_position if captured_position else end

    def castle(self, rook:Piece, start, end):
        self.is_castling_move = True
        self.rook = rook
        self.rook_start = start
        self.rook_end = end
        

    def __str__(self):
        return f"ChessMove {self.piece} from {self.start} to {self.end}, captured: {self.captured_piece} at {self.captured_position}, is_castling_move: {self.is_castling_move}"

    def __repr__(self):
        return f"ChessMove {self.piece} from {self.start} to {self.end}, captured: {self.captured_piece} at {self.captured_position}, is_castling_move: {self.is_castling_move}"
