from chess_move import ChessMove
from piece import Piece

class MoveGenerator:
    def __init__(self, board_state):
        self.board_state = board_state  # A 2D array representing the board

    def get_moves_for_piece(self, piece, start_position):
        if Piece.is_bishop(piece):
            return self.get_bishop_moves(piece, start_position)
        elif Piece.is_rook(piece):
            return self.get_rook_moves(piece, start_position)
        # Add other piece move generation as needed
        print ("unable to identify piece ", piece)
        return []

    def get_rook_moves(self, start_piece, start_position):
        print ("generating move for rook")
        moves = []
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Up, Right, Down, Left
        start_color = Piece.get_piece_color(start_piece)
        start_row, start_col = start_position
        
        for direction in directions:
            for i in range(1, 8):  # Rook can move up to 7 squares in one direction
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

    def get_bishop_moves(self, start_piece, start_position):
        print("generating move for bishop")
        # return [(0,0),(1,1),(2,2),(3,3),(4,4)]
    
        moves = []
        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]  # Diagonal directions
        start_row, start_col = start_position
        start_color = Piece.get_piece_color(start_piece)

        for direction in directions:
            for i in range(1, 8):  # Bishop can move up to 7 squares in one direction
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
