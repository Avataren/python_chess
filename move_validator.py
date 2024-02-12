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
        return True
                
    def validate_pawn_move(self, start_pos, end_pos, is_capture):
        # Implement pawn-specific logic, including promotion and en passant
        pass

    def validate_knight_move(self, start_pos, end_pos):
        # Implement knight movement logic
        pass
    
    def get_valid_moves(self, piece):
        if (piece & Piece.Bishop):
            return self.get_bishop_moves()
        # Implement logic to check if a move is legal
        # This involves checking the piece's movement rules, 
        # if the path is clear (for sliding pieces like rooks, bishops, and queens),
        # and if the move puts the player's own king in check.
        return []

    
    def validate_pawn_move(self, piece, start_pos, end_pos, is_capture, last_move=None):
        start_x, start_y = start_pos
        end_x, end_y = end_pos
        delta_x = end_x - start_x
        delta_y = end_y - start_y
        direction = 1 if piece.color == Piece.White else -1  # Determines movement direction based on piece color

        # Standard move and capture logic here...
        # Check for forward movement
        if delta_x == 0 and (delta_y == direction or (delta_y == 2 * direction and start_y == (6 if piece.color == Piece.White else 1))):
            if self.board_state[end_y][end_x] != Piece.No_Piece:
                return False  # Can't move forward into another piece
            if delta_y == 2 * direction and self.board_state[start_y + direction][start_x] != Piece.No_Piece:
                return False  # Can't jump over pieces
            return True

        # Check for captures
        if abs(delta_x) == 1 and delta_y == direction and is_capture:
            target_piece = self.board_state[end_y][end_x]
            if target_piece != Piece.No_Piece and target_piece.color != piece.color:
                return True  # Valid capture
            
        # En passant logic
        if abs(delta_x) == 1 and delta_y == direction and not is_capture:
            if (piece.color == Piece.White and start_y == 4) or (piece.color == Piece.Black and start_y == 3):  # Pawn is on the correct rank
                if last_move and last_move.piece == Piece.Pawn and abs(last_move.start[1] - last_move.end[1]) == 2:  # Last move was a two-square pawn move
                    if last_move.end == (start_x + delta_x, start_y):  # The last move ended adjacent to the current pawn
                        return True  # Valid en passant capture

        return False  # If none of the conditions are met, the move is illegal
    
    
    def validate_knight_move(self, start_pos, end_pos):
        start_x, start_y = start_pos
        end_x, end_y = end_pos
        delta_x = abs(end_x - start_x)
        delta_y = abs(end_y - start_y)

        return (delta_x == 2 and delta_y == 1) or (delta_x == 1 and delta_y == 2)  # Check for L-shape movement
    
    
