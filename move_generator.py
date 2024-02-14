import random
from chess_move import ChessMove
from piece import Piece

class MoveGenerator:
    
    rook_directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    bishop_directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
    queen_directions = [(1, 1), (1, -1), (-1, 1), (-1, -1),(0, 1), (1, 0), (0, -1), (-1, 0)]
    knight_directions = [(2, 1), (1, 2), (-1, 2), (-2, 1), (-2, -1), (-1, -2), (1, -2), (2, -1)]
    king_directions = [(1, 1), (1, 0), (1, -1), (0, 1), (0, -1), (-1, 1), (-1, 0), (-1, -1)]

    def get_all_moves(self, board_state, color):
        all_moves = []
        for row in range(8):
            for col in range(8):
                piece = board_state.board[row][col]
                if piece != Piece.No_Piece and Piece.get_piece_color(piece) == color:
                    moves = self.get_moves_for_piece(piece, (row, col), board_state)
                    if moves is not None:
                        for move in moves:
                            all_moves.append(ChessMove(piece,(row, col), move))
        sorted_moves = sorted(all_moves, key=lambda move: Piece.get_piece_value(move.piece))
                            
        return sorted_moves

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
            potential_moves += self.get_castling_moves(start_position, board_state, Piece.get_piece_color(piece))
            
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
        board_state.update_board(start_position, end_position)
        board_state.prepare()
        # If the moved piece is the king, update the king's position for the simulation
        if Piece.is_king(moved_piece):
            king_position = end_position
        # Check if the king is in check after the move
        in_check = self.is_king_in_check(Piece.get_piece_color(moved_piece), king_position, board_state)
        board_state.undo_last_move()
        #print ("in check: ", in_check, " for ", moved_piece, " from ", start_position, " to ", end_position, " king position: ", king_position, " board state:\n ", board_state.board)
        return in_check

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

        #print(f"Checking en passant for pawn at {start_position}")

        if board_state.last_move:
            from_row, from_col = board_state.last_move.start
            to_row, to_col = board_state.last_move.end
            #print(f"Last move: from {from_row},{from_col} to {to_row},{to_col}")

            if abs(from_row - to_row) == 2 and from_col == to_col:
                #print("Last move was a two-square pawn move.")
                if start_position[0] == to_row and abs(start_position[1] - to_col) == 1:
                    #print("En passant condition met.")
                    if Piece.get_piece_color(pawn) == Piece.White:
                        en_passant_target_row = to_row - 1  # For white pawns, move one row down
                    else:
                        en_passant_target_row = to_row + 1  # For black pawns, move one row up

                    en_passant_move = (en_passant_target_row, to_col)  # Target square for en passant
                    moves.append(en_passant_move)                     
                #else:
                #    print("Pawn not adjacent for en passant.")
            #else:
            #    ("Last move not eligible for en passant.")

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
    
    def get_attacked_squares(self, board_state, color):
            attacked_squares = set()  # Use a set to avoid duplicate entries
            for row in range(8):
                for col in range(8):
                    piece = board_state.board[row][col]
                    if piece != Piece.No_Piece and Piece.get_piece_color(piece) == color:
                        if Piece.is_pawn(piece):
                            # Pass row and col as separate arguments, not as a tuple or piece
                            attacked_squares.update(self.generate_pawn_capture_moves(row, col, color))
                        elif Piece.is_knight(piece):
                            attacked_squares.update(self.generate_moves(piece, (row, col), self.knight_directions, 1, board_state))
                        elif Piece.is_bishop(piece):
                            attacked_squares.update(self.generate_moves(piece, (row, col), self.bishop_directions, 8, board_state))
                        elif Piece.is_rook(piece):
                            attacked_squares.update(self.generate_moves(piece, (row, col), self.rook_directions, 8, board_state))
                        elif Piece.is_queen(piece):
                            attacked_squares.update(self.generate_moves(piece, (row, col), self.queen_directions, 8, board_state))
                        elif Piece.is_king(piece):
                            attacked_squares.update(self.generate_moves(piece, (row, col), self.king_directions, 1, board_state))
            return attacked_squares

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

    def is_checkmate(self, king_color, board_state):
        king_position = board_state.get_king_position(king_color)
        if not self.is_king_in_check(king_color, king_position, board_state):
            return False  # King is not in check, so it cannot be checkmate

        # Get all pieces for the king's color
        pieces_positions = board_state.white_positions if king_color == Piece.White else board_state.black_positions
        
        # Try all possible moves for all pieces of the king's color
        for row, col, piece in pieces_positions:
            start_position = (row, col)
            # Generate all possible moves for this piece
            possible_moves = self.get_moves_for_piece(piece, start_position, board_state)
            if possible_moves is None:
                continue
            
            for end_position in possible_moves:
                # Simulate the move
                board_state.update_board(start_position, end_position)
                board_state.prepare()
                # Check if the king is still in check after this move
                if not self.is_king_in_check(king_color, board_state.get_king_position(king_color), board_state):
                    board_state.undo_last_move()
                    return False  # Found a move that takes the king out of check, so it's not checkmate
                board_state.undo_last_move()

        return True  # No moves take the king out of check, so it's checkmate
    
    
    def is_path_clear_for_castling(self, start_position, end_position, board_state):
        """Check if there are no pieces between the start and end positions."""
        start_row, start_col = start_position
        end_row, end_col = end_position

        step = 1 if start_col < end_col else -1
        for col in range(start_col + step, end_col, step):
            if board_state.board[start_row][col] != Piece.No_Piece:
                return False
        return True

    def is_square_under_attack(self, square, target_color, board_state):
        # Determine the color of the opponent
        opponent_color = Piece.White if target_color == Piece.Black else Piece.Black

        # Iterate over all squares on the board to find opponent pieces
        for row in range(8):
            for col in range(8):
                piece = board_state.board[row][col]
                if piece != Piece.No_Piece and Piece.get_piece_color(piece) == opponent_color:
                    # Generate moves for this opponent piece
                    moves = self.get_moves_for_piece_without_check_detection(piece, (row, col), board_state)

                    # Check if any move targets the square in question
                    if square in moves:
                        return True

        # If no opponent moves target the square, it is not under attack
        return False


    def can_castle(self, king_position, rook_position, board_state, king_color):
        """Check if castling conditions are met."""
        if (self.is_king_in_check(king_color, king_position, board_state)):
            return False

        if not self.is_path_clear_for_castling(king_position, rook_position, board_state):
            return False

        # Check if the king moves through an attacked square
        direction = 1 if rook_position[1] > king_position[1] else -1
        for offset in range(1, 3):
            if self.is_square_under_attack((king_position[0], king_position[1] + offset * direction), king_color, board_state):
                return False

        return True
    
    def get_castling_moves(self, king_position, board_state, king_color):
        castling_moves = []
        color_key = 'K' if king_color == Piece.White else 'k'
        queenside_key = 'QR' if king_color == Piece.White else 'qr'
        kingside_key = 'KR' if king_color == Piece.White else 'kr'

        # Check for kingside castling
        if not board_state.has_moved[color_key] and not board_state.has_moved[kingside_key]:
            if self.can_castle(king_position, (king_position[0], 7), board_state, king_color):
                castling_moves.append((king_position[0], 6))  # King's destination

        # Check for queenside castling
        if not board_state.has_moved[color_key] and not board_state.has_moved[queenside_key]:
            if self.can_castle(king_position, (king_position[0], 0), board_state, king_color):
                castling_moves.append((king_position[0], 2))  # King's destination

        return castling_moves
    
    def select_random_valid_move(self, board_state, color):
        """
        Selects a random valid move for the given color.
        
        :param board_state: The current state of the chess board.
        :param color: The color (Piece.White or Piece.Black) for which to generate a move.
        :return: A random valid ChessMove or None if no valid moves are available.
        """
        all_valid_moves = self.get_all_moves(board_state, color)

        if not all_valid_moves:
            return None  # No valid moves available

        return random.choice(all_valid_moves)