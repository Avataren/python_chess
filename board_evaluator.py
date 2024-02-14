from move_generator import MoveGenerator
from piece import Piece


class BoardEvaluator:
    
    pawn_table = [
        0, 0, 0, 0, 0, 0, 0, 0,
        5, 10, 10, -20, -20, 10, 10, 5,
        5, -5, -10, 0, 0, -10, -5, 5,
        0, 0, 0, 20, 20, 0, 0, 0,
        5, 5, 10, 25, 25, 10, 5, 5,
        10, 10, 20, 30, 30, 20, 10, 10,
        50, 50, 50, 50, 50, 50, 50, 50,
        0, 0, 0, 0, 0, 0, 0, 0,
    ]

    knight_table = [
        -50, -40, -30, -30, -30, -30, -40, -50,
        -40, -20,   0,   5,   5,   0, -20, -40,
        -30,   5,  10,  15,  15,  10,   5, -30,
        -30,   0,  15,  20,  20,  15,   0, -30,
        -30,   5,  15,  20,  20,  15,   5, -30,
        -30,   0,  10,  15,  15,  10,   0, -30,
        -40, -20,   0,   0,   0,   0, -20, -40,
        -50, -40, -30, -30, -30, -30, -40, -50,
    ]

    bishop_table = [
        -20, -10, -10, -10, -10, -10, -10, -20,
        -10,   5,   0,   0,   0,   0,   5, -10,
        -10,  10,  10,  10,  10,  10,  10, -10,
        -10,   0,  10,  10,  10,  10,   0, -10,
        -10,   5,   5,  10,  10,   5,   5, -10,
        -10,   0,   5,  10,  10,   5,   0, -10,
        -10,   0,   0,   0,   0,   0,   0, -10,
        -20, -10, -10, -10, -10, -10, -10, -20,
    ]

    rook_table = [
        0, 0, 0, 5, 5, 0, 0, 0,
        -5, 0, 0, 0, 0, 0, 0, -5,
        -5, 0, 0, 0, 0, 0, 0, -5,
        -5, 0, 0, 0, 0, 0, 0, -5,
        -5, 0, 0, 0, 0, 0, 0, -5,
        -5, 0, 0, 0, 0, 0, 0, -5,
        5, 10, 10, 10, 10, 10, 10, 5,
        0, 0, 0, 0, 0, 0, 0, 0
    ]

    queen_table = [
        -20, -10, -10, -5, -5, -10, -10, -20,
        -10, 0, 0, 0, 0, 0, 0, -10,
        -10, 0, 5, 5, 5, 5, 0, -10,
        -5, 0, 5, 5, 5, 5, 0, -5,
        0, 0, 5, 5, 5, 5, 0, -5,
        -10, 5, 5, 5, 5, 5, 0, -10,
        -10, 0, 5, 0, 0, 0, 0, -10,
        -20, -10, -10, -5, -5, -10, -10, -20
    ]
    
    king_table = [
        20, 30, 10, 0, 0, 10, 30, 20,
        20, 20, 0, 0, 0, 0, 20, 20,
        -10, -20, -20, -20, -20, -20, -20, -10,
        -20, -30, -30, -40, -40, -30, -30, -20,
        -30, -40, -40, -50, -50, -40, -40, -30,
        -30, -40, -40, -50, -50, -40, -40, -30,
        -30, -40, -40, -50, -50, -40, -40, -30,
        -30, -40, -40, -50, -50, -40, -40, -30
    ]
    
    king_endgame_table = [
        -50, -40, -30, -20, -20, -30, -40, -50,
        -30, -20, -10, 0, 0, -10, -20, -30,
        -30, -10, 20, 30, 30, 20, -10, -30,
        -30, -10, 30, 40, 40, 30, -10, -30,
        -30, -10, 30, 40, 40, 30, -10, -30,
        -30, -10, 20, 30, 30, 20, -10, -30,
        -30, -30, 0, 0, 0, 0, -30, -30,
        -50, -30, -30, -30, -30, -30, -30, -50
    ]
    
    def evaluate(self, board_state, color):
        score = 0
        game_phase = self.determine_game_phase(board_state)

        # Adjust the base score based on piece positions and types
        active_positions = board_state.white_positions if color == Piece.White else board_state.black_positions
        for position in active_positions:
            r, c, piece = position
            table_index = r * 8 + c
            score += self.get_adjusted_piece_value(piece, table_index, game_phase)

        # Encourage piece development and center control
        # score += self.evaluate_piece_development(board_state, color) * 0.5
        # score += self.evaluate_center_control(board_state, color) * 0.5
        # Consider pawn structure in the evaluation
        #score += self.evaluate_pawn_structure(board_state, color) * 0.25

        # Evaluate mobility and threats
        #score += self.evaluate_mobility(board_state, color, active_positions)
        #score += self.evaluate_threats(board_state, color, active_positions)

        return score


    def get_adjusted_piece_value(self, piece, table_index, game_phase):
        base_value = Piece.get_piece_value(piece)
        color = Piece.get_piece_color(piece)
        table_scale = 1  # Adjust the scaling factor if necessary

        if Piece.is_pawn(piece):
            adjustment = self.pawn_table[table_index] if color == Piece.White else -self.pawn_table[63 - table_index]
        elif Piece.is_knight(piece):
            adjustment = self.knight_table[table_index] if color == Piece.White else -self.knight_table[63 - table_index]
        elif Piece.is_bishop(piece):
            adjustment = self.bishop_table[table_index] if color == Piece.White else -self.bishop_table[63 - table_index]
        elif Piece.is_rook(piece):
            adjustment = self.rook_table[table_index] if color == Piece.White else -self.rook_table[63 - table_index]
        elif Piece.is_queen(piece):
            adjustment = self.queen_table[table_index] if color == Piece.White else -self.queen_table[63 - table_index]
        elif Piece.is_king(piece):
            # Use the king's endgame table if in the endgame, otherwise use the standard king table
            if game_phase == 'endgame':
                adjustment = self.king_endgame_table[table_index] if color == Piece.White else -self.king_endgame_table[63 - table_index]
            else:
                adjustment = self.king_table[table_index] if color == Piece.White else -self.king_table[63 - table_index]
        else:
            # For unforeseen piece types, no adjustment is made
            adjustment = 0

        return base_value + adjustment * table_scale

    def adjust_pawn_table(self, table_index, game_phase):
        base_value = BoardEvaluator.pawn_table[table_index]
        if game_phase == 'early':
            # Reduce emphasis on central squares
            if table_index in [27, 28, 35, 36]:  # Central squares
                return base_value - 10  # Example reduction
        # No adjustment or different adjustments can be made for middle and endgame phases
        return base_value

    
    def determine_game_phase(self, board_state):
        # Count the number of queens and pawns as they significantly influence the game phase
        queen_count = sum(1 for row in board_state.board for piece in row if Piece.is_queen(piece))
        pawn_count = sum(1 for row in board_state.board for piece in row if Piece.is_pawn(piece))

        # Consider a game in the middle phase if there are fewer queens or many pawns, indicating more early-game conditions
        if queen_count < 2 or pawn_count > 12:
            return 'middle'
        # Adjust the thresholds as needed based on your game analysis
        elif pawn_count <= 8:
            return 'endgame'
        else:
            return 'early'
        
    def evaluate_piece_development(self, board_state, color):
        development_score = 0
        undeveloped_penalty = -10  # Penalty for each undeveloped piece

        # Correct starting positions for knights and bishops
        if color == Piece.White:
            undeveloped_positions = [(7, 1), (7, 6), (7, 2), (7, 5)]  # White's knights and bishops on the 8th rank (7th row in 0-indexed)
        else:
            undeveloped_positions = [(0, 1), (0, 6), (0, 2), (0, 5)]  # Black's knights and bishops on the 1st rank (0th row in 0-indexed)

        for r, c in undeveloped_positions:
            piece = board_state.board[r][c]
            if piece == Piece.No_Piece or Piece.get_piece_color(piece) != color:
                development_score += undeveloped_penalty

        return development_score

        
    def evaluate_center_control(self, board_state, color):
        center_squares = [(3, 3), (3, 4), (4, 3), (4, 4)]  # d4, d5, e4, e5
        center_control_score = 0
        center_control_bonus = 5  # Bonus for each piece controlling a center square

        # Instantiate MoveGenerator and get all attacked squares by the given color
        move_generator = MoveGenerator()
        attacked_squares = move_generator.get_attacked_squares(board_state, color)

        # Check if any center squares are in the set of attacked squares
        for center_square in center_squares:
            if center_square in attacked_squares:
                center_control_score += center_control_bonus

        return center_control_score


    def evaluate_pawn_structure(self, board_state, color):
        pawn_structure_score = 0
        doubled_pawn_penalty = -5
        isolated_pawn_penalty = -10
        backward_pawn_penalty = -3

        pawn_positions = board_state.get_pawn_positions(color)
        pawn_files = [c for r, c in pawn_positions]

        for r, c in pawn_positions:
            # Doubled pawns
            if pawn_files.count(c) > 1:
                pawn_structure_score += doubled_pawn_penalty

            # Isolated pawns
            if c == 0 or c == 7 or (c - 1 not in pawn_files and c + 1 not in pawn_files):
                pawn_structure_score += isolated_pawn_penalty

            # Backward pawns (simplified check)
            if r != (7 if color == Piece.White else 0) and (r + 1, c) not in pawn_positions:
                pawn_structure_score += backward_pawn_penalty

        return pawn_structure_score

    def evaluate_mobility(self, board_state, color, active_positions):
        mobility_score = 0
        mobility_bonus = 1  # Bonus for each legal move
        move_generator = MoveGenerator()
        for position in active_positions:
            piece = board_state.board[position[0]][position[1]]
            legal_moves = move_generator.get_moves_for_piece(piece, (position[0],position[1]), board_state)
            #board_state.get_legal_moves(position)
            mobility_score += len(legal_moves) * mobility_bonus

        return mobility_score
    
    def evaluate_threats(self, board_state, color, active_positions):
        threat_score = 0
        threat_bonus = 10  # Bonus for each threatened enemy piece
        threat_penalty = -20  # Penalty for each of the player's pieces being threatened
        moveGenerator = MoveGenerator()
        
        attacked_squares = moveGenerator.get_attacked_squares(board_state, color)
        
        # Threats made by the player's pieces
        for target in attacked_squares:
            if Piece.get_piece_color(board_state.board[target[0]][target[1]]) is not color:
                threat_score += threat_bonus

        for target in attacked_squares:
            if Piece.get_piece_color(board_state.board[target[0]][target[1]]) is color:
                threat_score += threat_penalty

        return threat_score
    