import numpy as np
from fen import FEN
from move_generator import MoveGenerator
from piece import Piece


class BoardState:
    board = np.empty((8, 8), dtype=Piece)
    move_history = []
    current_valid_moves = []
    selected_piece_position = None
    last_double_move = None
    fen = FEN()
    def __init__(self):
        self.reset_board()    

    def reset_board(self):
        self.current_fen_state = self.fen.initial_board_configuration
        self.board = self.fen.fen_to_board(self.current_fen_state)
    
    def is_move_legal(self, new_pos):
        col, row = new_pos
        if (self.current_valid_moves is not None):
            print ("valid moves available")
            if ((row, col) in self.current_valid_moves):
                print ("found valid position")
                return True
        else:
            print ("No moves available")
            
        return False    
    
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
        moveGenerator = MoveGenerator(self.board)
        self.current_valid_moves = moveGenerator.get_moves_for_piece(piece, (y,x)) # ensure row,col format
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