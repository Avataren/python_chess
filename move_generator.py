from piece import Piece

class MoveGenerator:
    
    rook_directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    bishop_directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
    queen_directions = [(1, 1), (1, -1), (-1, 1), (-1, -1),(0, 1), (1, 0), (0, -1), (-1, 0)]
    knight_directions = [(2, 1), (1, 2), (-1, 2), (-2, 1), (-2, -1), (-1, -2), (1, -2), (2, -1)]
    king_directions = [(1, 1), (1, 0), (1, -1), (0, 1), (0, -1), (-1, 1), (-1, 0), (-1, -1)]
    
    # def __init__(self):

    def get_moves_for_piece(self, piece, start_position, board_state):
        if Piece.is_bishop(piece):
            return self.generate_moves(piece, start_position, self.bishop_directions, 8, board_state)
        elif Piece.is_knight(piece):
            return self.generate_moves(piece, start_position, self.knight_directions, 2, board_state)
        elif Piece.is_rook(piece):
            return self.generate_moves(piece, start_position, self.rook_directions, 8, board_state)
        elif Piece.is_queen(piece):
            return self.generate_moves(piece, start_position, self.queen_directions, 8, board_state)
        elif Piece.is_king(piece):
            return self.generate_moves(piece, start_position, self.king_directions, 2, board_state)
        return self.generate_pawn_moves(piece, start_position, board_state)

    def generate_moves(self, start_piece, start_position, directions, max_range, board_state):
        moves = []
        start_color = Piece.get_piece_color(start_piece)
        start_row, start_col = start_position
        
        for direction in directions:
            for i in range(1, max_range):  # Rook can move up to 7 squares in one direction
                end_row = start_row + direction[0] * i
                end_col = start_col + direction[1] * i
                if 0 <= end_row < 8 and 0 <= end_col < 8:  # Ensure move is within board bounds
                    end_piece = board_state.board[end_row][end_col]
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


    def generate_pawn_moves(self, pawn, start_position, board_state):
        moves = []
        start_row, start_col = start_position
        color = Piece.get_piece_color(pawn)
        forward_one = forward_two = None

        if color == Piece.Black:  # Assuming Color is an enum or similar in your Piece class
            forward_one = start_row + 1
            forward_two = start_row + 2 if start_row == 1 else None  # Two steps forward only possible from starting position
        elif color == Piece.White:
            forward_one = start_row - 1
            forward_two = start_row - 2 if start_row == 6 else None

        # Forward moves
        if forward_one is not None and forward_one >= 0 and forward_one < 8:
            if board_state.board[forward_one][start_col] == Piece.No_Piece:
                moves.append((forward_one, start_col))
                if forward_two is not None and board_state.board[forward_two][start_col] == Piece.No_Piece:
                    moves.append((forward_two, start_col))

        # Diagonal Captures
        for col_offset in (-1, 1):
            capture_row = forward_one
            capture_col = start_col + col_offset
            if 0 <= capture_row < 8 and 0 <= capture_col < 8:
                capture_piece = board_state.board[capture_row][capture_col]
                if capture_piece != Piece.No_Piece and Piece.get_piece_color(capture_piece) != color:
                    moves.append((capture_row, capture_col))

        print(f"Checking en passant for pawn at {start_position}")

        if board_state.last_move:
            from_row, from_col = board_state.last_move.start
            to_row, to_col = board_state.last_move.end
            print(f"Last move: from {from_row},{from_col} to {to_row},{to_col}")

            if abs(from_row - to_row) == 2 and from_col == to_col:
                print("Last move was a two-square pawn move.")
                if start_position[0] == to_row and abs(start_position[1] - to_col) == 1:
                    print("En passant condition met.")
                    if Piece.get_piece_color(pawn) == Piece.White:
                        en_passant_target_row = to_row - 1  # For white pawns, move one row down
                    else:
                        en_passant_target_row = to_row + 1  # For black pawns, move one row up

                    en_passant_move = (en_passant_target_row, to_col)  # Target square for en passant
                    moves.append(en_passant_move)                     
                else:
                    print("Pawn not adjacent for en passant.")
            else:
                print("Last move not eligible for en passant.")

        return moves
