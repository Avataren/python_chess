import copy
import numpy as np
from board_evaluator import BoardEvaluator
from chess_move import ChessMove
from fen import FEN
from move_generator import MoveGenerator
from piece import Piece

class BoardState:
    board = np.empty((8, 8), dtype=Piece)
    move_history = []
    current_valid_moves = []
    selected_piece_position = None
    last_move: ChessMove = None
    has_moved = {'K': False, 'Q': False, 'k': False, 'q': False, 'KR': False, 'QR': False, 'kr': False, 'qr': False}  # Track if kings and rooks have moved for castling

    black_positions = []
    white_positions = []
    king_position_black = None
    king_position_white = None
    
    current_player_color = Piece.White
    
    fen = FEN()
    def __init__(self):
        self.reset_board()    

    def reset_board(self):
        self.current_fen_state = self.fen.initial_board_configuration
        self.board = self.fen.fen_to_board(self.current_fen_state)
        self.has_moved = {'K': False, 'Q': False, 'k': False, 'q': False, 'KR': False, 'QR': False, 'kr': False, 'qr': False}  # Track if kings and rooks have moved for castling
        self.last_double_move = None
        self.prepare()
    
    def end_current_turn(self):
        print ("Board evaluation is ", BoardEvaluator.evaluate(self))
        self.current_player_color = Piece.Black if self.current_player_color == Piece.White else Piece.White
    
    def is_move_legal(self, new_pos):
        row, col = new_pos
        if (self.current_valid_moves is not None):
            print ("valid moves available")
            if ((row, col) in self.current_valid_moves):
                print ("found valid position")
                return True
        else:
            print ("No moves available")
            
        return False    
    
    def execute_move(self, piece: Piece, old_position, new_position):
        if (self.current_player_color != Piece.get_piece_color(piece)):
            print ("Not your turn")
            return
        
        print(f"Executing move from {old_position} to {new_position}")
        
        # Handle castling logic
        if Piece.is_king(piece) and abs(new_position[1] - old_position[1]) == 2:
            self.handle_castling(old_position, new_position)
        
        # Normal move execution
        self.update_board(piece, old_position, new_position)
        
        # Update has_moved dictionary
        if Piece.is_king(piece):
            self.has_moved['K' if Piece.get_piece_color(piece) == Piece.White else 'k'] = True
        elif Piece.is_rook(piece):
            if old_position == (7, 0) or old_position == (0, 0):  # Queenside rook
                self.has_moved['QR' if Piece.get_piece_color(piece) == Piece.White else 'qr'] = True
            elif old_position == (7, 7) or old_position == (0, 7):  # Kingside rook
                self.has_moved['KR' if Piece.get_piece_color(piece) == Piece.White else 'kr'] = True
        # Record the move
        self.last_move = ChessMove(piece, old_position, new_position)
        self.end_current_turn()

    def handle_castling(self, old_king_position, new_king_position):
        direction = 1 if new_king_position[1] - old_king_position[1] > 0 else -1
        rook_old_col = 7 if direction == 1 else 0
        rook_new_col = new_king_position[1] - direction  # Rook moves to the adjacent column of the king's new position
        rook_position = (old_king_position[0], rook_old_col)
        new_rook_position = (new_king_position[0], rook_new_col)
        # Move the rook
        self.update_board(self.board[rook_position[0]][rook_position[1]], rook_position, new_rook_position)

    def handle_special_moves(self, piece: Piece, old_position, new_position):
        if self.is_en_passant(piece, old_position, new_position):
            self.remove_captured_pawn_en_passant(new_position)

    def is_en_passant(self, piece: Piece, old_position, new_position):
        if (piece & 7) != Piece.Pawn:
            return False

        last_move = self.last_move
        if not (last_move and abs(last_move.start[0] - last_move.end[0]) == 2 and (piece & 8) != (last_move.piece & 8)):
            return False

        return abs(new_position[1] - old_position[1]) == 1 and \
               ((Piece.get_piece_color(piece) == Piece.White and new_position[0] == last_move.end[0] - 1) or
                (Piece.get_piece_color(piece) == Piece.Black and new_position[0] == last_move.end[0] + 1))

    def remove_captured_pawn_en_passant(self, new_position):
        last_move = self.last_move
        captured_pawn_position = (last_move.end[0], new_position[1])
        print("En passant capture detected!")
        self.board[captured_pawn_position[0]][captured_pawn_position[1]] = Piece.No_Piece

    def update_board(self, piece: Piece, old_position, new_position):
        self.board[new_position[0]][new_position[1]] = piece
        self.board[old_position[0]][old_position[1]] = Piece.No_Piece

    def take_piece_at_position(self, position, square_size):
        # Logic to get the piece at the given position
        mouseX, mouseY = position
        x = int(mouseX // square_size)
        y = int(mouseY // square_size)
        if (x < 0 or x > 7 or y < 0 or y > 7):
            self.current_valid_moves = None
            return None
        piece = self.board[y][x]
        if (self.current_player_color != Piece.get_piece_color(piece)):
            print ("Not your turn")
            return Piece.No_Piece
        
        self.selected_piece_position = (y,x)
        moveGenerator = MoveGenerator()
        self.current_valid_moves = moveGenerator.get_moves_for_piece(piece, (y,x), self) # ensure row,col format
        print (f"valid moves:{self.current_valid_moves}")
        self.board[y][x] = Piece.No_Piece
        return piece    

    def prepare(self):
        self.black_positions = list(self.get_all_pieces_positions_by_color(Piece.Black, self))
        self.white_positions = list(self.get_all_pieces_positions_by_color(Piece.White, self))
        self.king_position_black = next(((row, col) for row, col, piece in self.black_positions if piece == Piece.BlackKing), None)
        self.king_position_white = next(((row, col) for row, col, piece in self.white_positions if piece == Piece.WhiteKing), None)
        print("king positions (black,white)", self.king_position_black, self.king_position_white)
            
    get_king_position = lambda self, color: self.king_position_black if color == Piece.Black else self.king_position_white
    
    def get_all_pieces_positions_by_color(self, color, board_state):
        for row in range(8):
            for col in range(8):
                piece = board_state.board[row][col]
                if Piece.get_piece_color(piece) == color:
                    yield (row, col, piece)    
    
    def move_piece(self, start_position, end_position):
        piece = self.board[start_position[0]][start_position[1]]
        self.execute_move(piece, start_position, end_position)
        self.current_valid_moves = None
    
    def copy(self):
        # Create a new BoardState instance
        new_board_state = BoardState()
        
        # Directly copy immutable and simple mutable objects
        new_board_state.board = np.copy(self.board)  # Deep copy of the board array
        new_board_state.move_history = copy.deepcopy(self.move_history) if self.move_history is not None else None  # Deep copy with None check
        new_board_state.current_valid_moves = list(self.current_valid_moves) if self.current_valid_moves is not None else None  # Shallow copy with None check
        new_board_state.selected_piece_position = self.selected_piece_position  # Tuples are immutable, direct copy is fine
        new_board_state.last_move = copy.deepcopy(self.last_move) if self.last_move is not None else None  # Deep copy with None check
        new_board_state.has_moved = self.has_moved.copy() if self.has_moved is not None else None  # Shallow copy of the dictionary with None check
        new_board_state.black_positions = list(self.black_positions) if self.black_positions is not None else None  # Shallow copy with None check
        new_board_state.white_positions = list(self.white_positions) if self.white_positions is not None else None  # Shallow copy with None check
        new_board_state.king_position_black = self.king_position_black  # Tuples are immutable, direct copy is fine
        new_board_state.king_position_white = self.king_position_white  # Tuples are immutable, direct copy is fine

        return new_board_state    
    
    def debug_print_board(self):
        """
        Prints the board configuration in text format.
        """
        print("  a b c d e f g h")
        print(" +-----------------+")
        for i, row in enumerate(self.board):
            print(f"{8 - i} | {' '.join(self.fen.get_fen_char_from_piece(piece) for piece in row)} | {8 - i}")
        print(" +-----------------+")
        print("  a b c d e f g h")    