import numpy as np
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

    fen = FEN()
    def __init__(self):
        self.reset_board()    

    def reset_board(self):
        self.current_fen_state = self.fen.initial_board_configuration
        self.board = self.fen.fen_to_board(self.current_fen_state)
        self.has_moved = {'K': False, 'Q': False, 'k': False, 'q': False, 'KR': False, 'QR': False, 'kr': False, 'qr': False}  # Track if kings and rooks have moved for castling
        self.last_double_move = None
        
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
        print(f"Executing move from {old_position} to {new_position}")
        
        # Check for and handle special moves like en passant
        self.handle_special_moves(piece, old_position, new_position)
        # Execute the move
        self.update_board(piece, old_position, new_position)
        # Record the move
        self.last_move = ChessMove(piece, old_position, new_position)

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
        self.selected_piece_position = (y,x)
        moveGenerator = MoveGenerator()
        self.current_valid_moves = moveGenerator.get_moves_for_piece(piece, (y,x), self) # ensure row,col format
        print (f"valid moves:{self.current_valid_moves}")
        self.board[y][x] = Piece.No_Piece
        return piece    
    
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