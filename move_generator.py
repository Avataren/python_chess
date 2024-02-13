from piece import Piece

class MoveGenerator:
    
    rook_directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    bishop_directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
    queen_directions = [(1, 1), (1, -1), (-1, 1), (-1, -1),(0, 1), (1, 0), (0, -1), (-1, 0)]
    knight_directions = [(2, 1), (1, 2), (-1, 2), (-2, 1), (-2, -1), (-1, -2), (1, -2), (2, -1)]
    king_directions = [(1, 1), (1, 0), (1, -1), (0, 1), (0, -1), (-1, 1), (-1, 0), (-1, -1)]

    def get_moves_for_piece(self, piece, start_position, board_state):
        if piece is None or piece == Piece.No_Piece or start_position is None or board_state is None:
            return None
        potential_moves = []
        board_state.prepare()
        # Generate all potential moves for the piece
        if Piece.is_bishop(piece):
            potential_moves = self.generate_moves(piece, start_position, self.bishop_directions, 8, board_state)
        elif Piece.is_knight(piece):
            potential_moves = self.generate_moves(piece, start_position, self.knight_directions, 2, board_state)
        elif Piece.is_rook(piece):
            potential_moves = self.generate_moves(piece, start_position, self.rook_directions, 8, board_state)
        elif Piece.is_queen(piece):
            potential_moves = self.generate_moves(piece, start_position, self.queen_directions, 8, board_state)
        elif Piece.is_king(piece):
            potential_moves = self.generate_moves(piece, start_position, self.king_directions, 2, board_state)
        else:
            potential_moves = self.generate_pawn_moves(piece, start_position, board_state)

        # Filter out moves that leave the king in check
        valid_moves = []
        king_position = board_state.get_king_position(Piece.get_piece_color(piece))
        for move in potential_moves:
            if not self.does_move_leave_king_in_check(piece, start_position, move, king_position, board_state):
                valid_moves.append(move)

        return valid_moves

    def get_moves_for_piece_without_check_detection(self, piece, start_position, board_state):
        if piece is None or piece == Piece.No_Piece or start_position is None or board_state is None:
            return None
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
        else:
            return self.generate_pawn_moves(piece, start_position, board_state)

    def does_move_leave_king_in_check(self, moved_piece, start_position, end_position, king_position, board_state):
            # Create a copy of the board to simulate the move
            board_copy = board_state.copy()  # Assuming this method exists to create a deep copy of the board state
            board_copy.move_piece(start_position, end_position)  # Assuming this method exists to update the board
            # If the moved piece is the king, update the king's position for the simulation
            if Piece.is_king(moved_piece):
                king_position = end_position
            # Check if the king is in check after the move
            return self.is_king_in_check(Piece.get_piece_color(moved_piece), king_position, board_copy)

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
    
    def can_pawn_capture_king(self, pawn_row, pawn_col, king_position, pawn_color):
        capture_moves = self.generate_pawn_capture_moves(pawn_row, pawn_col, pawn_color)
        return king_position in capture_moves    

    def generate_pawn_capture_moves(self, row, col, color):
        moves = []
        if color == Piece.Black:
            potential_moves = [(row + 1, col - 1), (row + 1, col + 1)]
        else:
            potential_moves = [(row - 1, col - 1), (row - 1, col + 1)]

        for move in potential_moves:
            if 0 <= move[0] < 8 and 0 <= move[1] < 8:  # Ensure move is within board bounds
                moves.append(move)
        return moves    
    
    def is_king_in_check(self, king_color, king_position, board_state):
        opponent_color = Piece.Black if king_color == Piece.White else Piece.White
        
        opponent_pieces_positions = board_state.black_positions if king_color == Piece.White else board_state.white_positions

        for positioned_piece in opponent_pieces_positions:
            row, col , opponent_piece = positioned_piece
            if Piece.is_pawn(opponent_piece):
                if self.can_pawn_capture_king(row, col, king_position, opponent_color):
                    return True
            else:
                moves = self.get_moves_for_piece_without_check_detection(opponent_piece, (row, col), board_state)
                if moves is not None:
                    if king_position in moves:
                        return True
        return False