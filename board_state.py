import copy
import pickle
import numpy as np
from board_evaluator import BoardEvaluator
from chess_move import ChessMove
from fen import FEN
from move_generator import MoveGenerator
from piece import Piece

class BoardState:
    board = np.empty((8, 8), dtype=Piece)
    current_valid_moves = []
    selected_piece_position = None
    has_moved = {'K': False, 'Q': False, 'k': False, 'q': False, 'KR': False, 'QR': False, 'kr': False, 'qr': False}  # Track if kings and rooks have moved for castling
    is_game_over = False
    black_positions = []
    white_positions = []
    move_number = {Piece.Black:0, Piece.White:0}
    current_player_color = Piece.White
    captured_en_passant = None
    captured_en_passant_position = None
    castling_rook_position_start = None
    castling_rook_position_end = None
    castling_rook = None
    
    fen = FEN()
    def __init__(self):
        self.reset_board()
    move_history = []

    def save(self):
        data_to_save = {
            'fen': self.fen.board_state_to_fen(self),
            'move_history': self.move_history
        }
        with open("game.chs", "wb") as file:
            pickle.dump(data_to_save, file)

    def load(self):
        with open("game.chs", "rb") as file:
            loaded_data = pickle.load(file)
        fen_state = loaded_data['fen']
        self.fen.fen_to_board_state(fen_state, self)
        self.move_history = loaded_data['move_history']
        
    def reset_board(self):
        self.current_fen_state = self.fen.initial_board_configuration
        self.fen.fen_to_board_state(self.current_fen_state, self)
        self.last_double_move = None
        self.current_player_color = Piece.White
        self.is_game_over = False
        self.move_number = {Piece.Black:0, Piece.White:0}
        self.captured_en_passant = None
        self.captured_en_passant_position = None        

    def num_moves_without_capture(self):
        return max(self.move_number[Piece.White], self.move_number[Piece.Black])
    
    def end_turn(self):
        self.current_player_color = Piece.get_opposite_color(self.current_player_color)
        #print ("end turn")
        #print (self.current_player_color)
        if (self.current_player_color == Piece.White):
            self.move_number[Piece.White] += 1
        else:
            self.move_number[Piece.Black] += 1
            
        board_mover = MoveGenerator()
        #self.prepare() # is this needed?
        if (board_mover.is_checkmate(self.current_player_color, self)):
            #print ("Checkmate!")
            self.end_game()
    
    def is_move_legal(self, new_pos):
        row, col = new_pos
        if self.current_valid_moves:
            print("Valid moves available")
            for move in self.current_valid_moves:
                if (move.end[0], move.end[1]) == (row, col):
                    print("Found valid position")
                    return True
        else:
            print("No moves available")

        return False
    
    def get_piece(self, row, col):
        return self.board[row][col] 
    
    def execute_move(self, move: ChessMove):

        # Handle castling logic
        if Piece.is_king(move.piece) and abs(move.start[1] - move.end[1]) == 2:
            self.handle_castling(move.start, move.end)
        
        #en passant
        self.handle_special_moves(move.piece, move.start, move.end)
        self.update_board(move.start, move.end, move.piece)

        # Update has_moved dictionary after update_move to get castling rights correct in history
        piece_color = Piece.get_piece_color(move.piece)
        if Piece.is_king(move.piece):
            self.has_moved['K' if piece_color == Piece.White else 'k'] = True
        elif Piece.is_rook(move.piece):
            if move.start == (7, 0) or move.start == (0, 0):  # Queenside rook
                self.has_moved['QR' if piece_color == Piece.White else 'qr'] = True
            elif move.start == (7, 7) or move.start == (0, 7):  # Kingside rook
                self.has_moved['KR' if piece_color == Piece.White else 'kr'] = True

        # Record the move
        self.end_turn()
        
    def update_board(self, old_position, new_position, use_piece=None):
        #Handle pawn promotion, only queen for now
        piece = use_piece if use_piece is not None else self.board[old_position[0]][old_position[1]]
        if (piece == Piece.No_Piece):
            return

        activePiece = piece
        if (piece&7) == Piece.Pawn:
            color = Piece.get_piece_color(piece)
            if (new_position[0] == 0 and color == Piece.White):
                #print ("Promoting pawn to queen at position ", new_position)
                activePiece = Piece.WhiteQueen
            elif (new_position[0] == 7 and color == Piece.Black):
                #print ("Promoting pawn to queen at position ", new_position)
                activePiece = Piece.BlackQueen

        captured_piece = self.board[new_position[0]][new_position[1]]
        move = ChessMove(piece, old_position, new_position, captured_piece)

        if self.captured_en_passant is not None:
            #print ("Adding en passant to move history")
            move = ChessMove(piece, old_position, new_position, self.captured_en_passant, self.captured_en_passant_position)
            self.captured_en_passant = None
            self.captured_en_passant_position = None
            
        elif (self.castling_rook_position_start is not None):
            move.castle(self.board[self.castling_rook_position_start[0]][self.castling_rook_position_start[1]],self.castling_rook_position_start, self.castling_rook_position_end)
            self.board[self.castling_rook_position_end[0]][self.castling_rook_position_end[1]] = self.board[self.castling_rook_position_start[0]][self.castling_rook_position_start[1]]
            self.board[self.castling_rook_position_start[0]][self.castling_rook_position_start[1]] = Piece.No_Piece            
            self.castling_rook_position_start = None
            self.castling_rook_position_end = None
            self.castling_rook = None        
                
            
        self.move_history.append((move, self.has_moved.copy()))
        #print (f"last move: {self.last_move}, placing active piece: {activePiece}")
        self.board[new_position[0]][new_position[1]] = activePiece
        self.board[old_position[0]][old_position[1]] = Piece.No_Piece

    def undo_last_move(self):
        
        if (len(self.move_history) > 0):
            last_move, has_moved = self.move_history.pop()
            # print ("##### undoing last move", last_move)
            self.has_moved = has_moved.copy()
            self.board[last_move.end[0]][last_move.end[1]] = Piece.No_Piece # Clear the destination in case its not the same as captured position
            self.board[last_move.captured_position[0]][last_move.captured_position[1]] = last_move.captured_piece
            self.board[last_move.start[0]][last_move.start[1]] = last_move.piece
            
            if (last_move.is_castling_move):
                self.board[last_move.rook_end[0]][last_move.rook_end[1]] = Piece.No_Piece
                self.board[last_move.rook_start[0]][last_move.rook_start[1]] = last_move.rook

            
            self.current_player_color = Piece.get_piece_color(last_move.piece)
        else:
            print ("No moves to undo")

    def end_game(self):
        self.is_game_over = True

    def handle_castling(self, old_king_position, new_king_position):
        #print ("Castling detected!")
        direction = 1 if new_king_position[1] - old_king_position[1] > 0 else -1
        rook_old_col = 7 if direction == 1 else 0
        rook_new_col = new_king_position[1] - direction  # Rook moves to the adjacent column of the king's new position
        rook_position = (old_king_position[0], rook_old_col)
        new_rook_position = (new_king_position[0], rook_new_col)
        self.castling_rook_position_start = rook_position
        self.castling_rook_position_end = new_rook_position

        # Move the rook, don't update history with update_board, since this will be recorded as one move later
       
        #self.update_board(rook_position, new_rook_position)

    def handle_special_moves(self, piece: Piece, old_position, new_position):
        if self.is_en_passant(piece, old_position, new_position):
            self.remove_captured_pawn_en_passant(old_position, new_position)
        else:
            self.captured_en_passant = None
            self.captured_en_passant_position = None

    def is_en_passant(self, piece: Piece, old_position, new_position):
        if (piece & 7) != Piece.Pawn:
            return False
        piece_color = Piece.get_piece_color(piece)
        last_move = self.move_history[-1][0] if len(self.move_history) > 0 else None
        if (last_move is None):
            return False
        if (last_move and abs(last_move.start[0] - last_move.end[0]) == 2):
            if  piece_color == Piece.get_piece_color(last_move.piece):
                return False

        if piece_color == Piece.White:
            expected_rank = last_move.end[0] - 1  # For white pawn, it should move to the rank just behind the black pawn
        else:
            expected_rank = last_move.end[0] + 1  # For black pawn, it should move to the rank just behind the white pawn

        return abs(new_position[1] - old_position[1]) == 1 and new_position[0] == expected_rank

    def remove_captured_pawn_en_passant(self, old_position, new_position):
        # Use old_position[0] for the rank and new_position[1] for the file
        captured_pawn_position = (old_position[0], new_position[1])
        self.captured_en_passant = self.board[captured_pawn_position[0]][captured_pawn_position[1]]
        self.captured_en_passant_position = captured_pawn_position
        self.board[captured_pawn_position[0]][captured_pawn_position[1]] = Piece.No_Piece
        #print("En passant capture detected and piece removed!")


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
        board_copy = self.board.copy()
        self.current_valid_moves = moveGenerator.get_moves_for_piece((y,x), self) # ensure row,col format
        print ("IS BOARD IDENTICAL: ", self.compare_to_board(board_copy))
        # print (f"valid moves:{self.current_valid_moves}")
        self.board[y][x] = Piece.No_Piece
        return piece    

    def compare_to_board(self, board2):
        for row in range(8):
            for col in range(8):
                if (self.board[row][col] != board2[row][col]):
                    return False
        return True

    def get_king_position(self, color):
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                piece_color = Piece.get_piece_color(piece)
                if Piece.is_black_king(piece) and color == Piece.Black:
                    return (row, col)
                elif Piece.is_white_king(piece) and color == Piece.White:
                    return (row, col)
        return None  # King not found (shouldn't happen in a valid game state)
        
    def get_all_pieces_positions_by_color(self, color):
        pieces = []
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece == Piece.No_Piece:
                    continue
                if Piece.get_piece_color(piece) == color:
                    #yield (row, col, piece)
                    pieces.append((row, col, piece))
        return pieces

    
    def get_pawn_positions(self, color):
        for (row, col, piece) in self.get_all_pieces_positions_by_color(color):
            if Piece.is_pawn(piece):
                yield (row, col)
    
    def make_move(self, move):
        self.execute_move(move)
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
        new_board_state.current_player_color = self.current_player_color  # Immutable, direct copy is fine
        new_board_state.is_game_over = self.is_game_over
        new_board_state.move_number = self.move_number.copy()
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