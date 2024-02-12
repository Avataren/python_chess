from chess_move import ChessMove
from piece import Piece

class MoveGenerator:
    rook_directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    bishop_directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
    queen_directions = [(1, 1), (1, -1), (-1, 1), (-1, -1),(0, 1), (1, 0), (0, -1), (-1, 0)]
    knight_directions = [(2, 1), (1, 2), (-1, 2), (-2, 1), (-2, -1), (-1, -2), (1, -2), (2, -1)]
    king_directions = [(1, 1), (1, 0), (1, -1), (0, 1), (0, -1), (-1, 1), (-1, 0), (-1, -1)]
    
    def __init__(self, board_state):
        self.board_state = board_state  # A 2D array representing the board

    def get_moves_for_piece(self, piece, start_position):
        if Piece.is_bishop(piece):
            return self.generate_moves(piece, start_position, self.bishop_directions)
        if Piece.is_knight(piece):
            return self.generate_moves(piece, start_position, self.knight_directions, 2)
        elif Piece.is_rook(piece):
            return self.generate_moves(piece, start_position, self.rook_directions)
        elif Piece.is_queen(piece):
            return self.generate_moves(piece, start_position, self.queen_directions)
        elif Piece.is_king(piece):
            return self.generate_moves(piece, start_position, self.king_directions, 2)
        return self.generate_pawn_moves(piece, start_position)

    def generate_moves(self, start_piece, start_position, directions, max_range=8):
        moves = []
        start_color = Piece.get_piece_color(start_piece)
        start_row, start_col = start_position
        
        for direction in directions:
            for i in range(1, max_range):  # Rook can move up to 7 squares in one direction
                end_row = start_row + direction[0] * i
                end_col = start_col + direction[1] * i
                if 0 <= end_row < 8 and 0 <= end_col < 8:  # Ensure move is within board bounds
                    end_piece = self.board_state[end_row][end_col]
                    end_color = Piece.get_piece_color(end_piece)
                    if end_piece == Piece.No_Piece:  # Empty square, valid move
                        moves.append((end_row, end_col))
                    elif end_color != start_color:  # Capture
                        moves.append((end_row, end_col))
                        break  # Blocked by a piece, can't move further in this direction
                    else:
                        break  # Blocked by own piece
                else:
                    break  # Move is outside the board
        return moves
    
    def generate_pawn_moves(self, pawn, start_position):
        moves = []
        start_row, start_col = start_position
        color = Piece.get_piece_color(pawn)

        # One or two steps forward based on starting rank
        if color == Piece.Black:
            forward_one = start_row + 1
            forward_two = start_row + 2
        else:  # BLACK
            forward_one = start_row - 1
            forward_two = start_row - 2

        # Forward moves
        if 0 <= forward_one < 8 and self.board_state[forward_one][start_col] == Piece.No_Piece:
            moves.append((forward_one, start_col))
            if start_row in (1, 6) and self.board_state[forward_two][start_col] == Piece.No_Piece:
                moves.append((forward_two, start_col))

        # Diagonal Captures
        for col_offset in (-1, 1):
            capture_row = forward_one
            capture_col = start_col + col_offset
            if 0 <= capture_row < 8 and 0 <= capture_col < 8:
                capture_piece = self.board_state[capture_row][capture_col]
                if capture_piece != Piece.No_Piece and Piece.get_piece_color(capture_piece) != color:
                    moves.append((capture_row, capture_col))

        # En Passant
        # if start_row in (4, 3):  # Pawn must be on rank 5 or 4
        #     for col_offset in (-1, 1):
        #         neighbor_col = start_col + col_offset
        #         if 0 <= neighbor_col < 8:
        #             neighbor_pawn = self.board_state[start_row][neighbor_col]
        #             if (Piece.is_pawn(neighbor_pawn) and
        #                     Piece.get_piece_color(neighbor_pawn) != color and
        #                     # Add logic to check for 'last_double_move' in board history):
        #                     self.board_state.last_double_move == (start_row, neighbor_col)): 
        #                 moves.append((forward_one, neighbor_col))  # En passant capture square

        return moves
       
