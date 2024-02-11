from typing import Optional
from piece import Piece

class MoveValidator:
    def __init__(self, board_state):
        self.board_state = board_state  # A 2D array representing the board

    def is_move_legal(self, piece:Optional[Piece], start_pos, end_pos):
        if piece is None:
            return False
        x,y = end_pos
        if (x < 0 or x > 7 or y < 0 or y > 7):
            return False
        if self.board_state[y][x] != Piece.No_Piece:
            return False
        
        # Implement logic to check if a move is legal
        # This involves checking the piece's movement rules, 
        # if the path is clear (for sliding pieces like rooks, bishops, and queens),
        # and if the move puts the player's own king in check.
        return True
        
    def validate_pawn_move(self, start_pos, end_pos, is_capture):
        # Implement pawn-specific logic, including promotion and en passant
        pass

    def validate_knight_move(self, start_pos, end_pos):
        # Implement knight movement logic
        pass
