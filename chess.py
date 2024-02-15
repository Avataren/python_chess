import pygame
from typing import Optional
from board_drawer import BoardDrawer
from board_state import BoardState
from chess_ai import ChessAI
from chess_move import ChessMove
from fen import FEN
from move_generator import MoveGenerator
from piece_drawer import PieceDrawer
from piece import Piece

class Chess:
    debug = False
    board_size = 720
    square_size = board_size / 8
    LIGHT_SQUARE_COLOR = "#F0D9B5"
    DARK_SQUARE_COLOR = "#B58863"
    SELECTED_SQAURE_COLOR = "#EE5544"
    VALID_MOVE_COLOR = "#33333333"
    selected_piece:Optional[Piece] = None
    selected_piece_position = None
    dragging = False    
    drag_position = None
    fen = FEN()
    board_state = BoardState()
    selected_grid_position = None
    board_surface = None
    ai = ChessAI(4)
    
    def __init__(self, board_size):
        print("Chess game initialized")
        self.board_size = board_size
        self.square_size = board_size // 8
        self.board_drawer = BoardDrawer(self.board_size, self.square_size)
        self.pieceDrawer = PieceDrawer("assets/pieces.png")
        self.reset_board()

    def reset_board(self):
        self.board_state.reset_board()

    def pick_up_piece(self, mousePosition):
        if (self.dragging):
            print ("Already dragging a piece")
            return
        print ("##############################################")
        piece = self.board_state.take_piece_at_position(mousePosition, self.square_size)
        if (piece is Piece.No_Piece):
            #will fail if not current players turn
            return
        
        print (f"Selected piece: {piece}")
        self.selected_piece = piece
        mouseX, mouseY = mousePosition
        x = int(mouseX // self.square_size)
        y = int(mouseY // self.square_size)
        self.selected_grid_position = (x, y) if self.selected_piece is not Piece.No_Piece else None    
        self.drag_position = (x * self.square_size , y * self.square_size)
        self.dragging = piece is not Piece.No_Piece and piece is not None

    def get_square_location_from_position(self, position):
        posX, posY = position
        return ( int(posY // self.square_size), int(posX // self.square_size))

    def get_piece_at_position(self, mousePosition):
        row,col = self.get_square_location_from_position(mousePosition)
        if (col < 0 or col > 7 or row < 0 or row > 7):
            return None
        return self.board_state.board[row][col]
    
    def deselect_piece(self):
        self.selected_piece = None
        self.selected_grid_position = None
        self.dragging = False
        self.drag_position = None
        self.selected_piece_position = None
    
    def move_piece(self, mousePosition):
        if self.dragging is False:
            return
        print ("MAKING A MOVE!")
        # Logic to move a piece to a new position if the move is legal
        new_position = self.get_square_location_from_position(mousePosition)
        old_position = self.board_state.selected_piece_position
        if self.selected_piece and self.board_state.is_move_legal(new_position):
            print ("Executing move!")
            self.board_state.make_move(ChessMove(self.selected_piece, old_position, new_position))
            self.deselect_piece()
            #self.do_next_ai_move()
        else:
            print("Illegal move")
            row, col = self.board_state.selected_piece_position
            self.board_state.board[row][col] = self.selected_piece
            self.selected_piece = None
            self.dragging = False
            self.drag_position = None
        self.board_state.current_valid_moves = None
            
    def save_fen_state(self):
        fen = self.fen.board_to_fen(self.board_state.board)
        file = open("fen.txt", "w")
        file.write(fen)
        file.close()

    def load_fen_state(self):
        self.reset_board()
        file = open("fen.txt", "r")
        fen = file.read()
        self.board_state.board = self.fen.fen_to_board(fen)

    def update_dragging_piece_position(self, mousePosition):
        self.drag_position = (mousePosition[0] - self.square_size / 2, mousePosition[1] - self.square_size / 2)
    
        col,row = self.get_square_location_from_position(mousePosition)
        moveGenerator = MoveGenerator()
        if (self.debug):
            self.board_state.current_valid_moves = moveGenerator.get_moves_for_piece(self.selected_piece, (row, col), self.board_state.board)
        
    def draw_dragged_piece(self, screen):
        if self.drag_position is not None and self.selected_piece is not None:
            self.pieceDrawer.draw_piece(screen, self.selected_piece, self.drag_position, (self.square_size, self.square_size))
    
    # def draw(self, screen):
    #     self.board_drawer.draw_board(screen)
    #     self.board_drawer.draw_valid_moves(screen, self.board_state.current_valid_moves)
    #     # self.draw_board(screen)
    #     self.draw_pieces_from_fen(screen, self.fen.board_to_fen(self.board_state.board))
    #     if (self.dragging):
    #         self.board_drawer.highlight_square(screen, self.selected_grid_position)
    #         self.draw_dragged_piece(screen)

    def draw(self, screen, custom_board_state = None):
        if (custom_board_state is None):
            custom_board_state = self.board_state
        self.board_drawer.draw_board(screen)
        self.board_drawer.draw_valid_moves(screen, custom_board_state.current_valid_moves)
        # self.draw_board(screen)
        self.draw_pieces_from_fen(screen, self.fen.board_to_fen(custom_board_state.board))
        if (self.dragging):
            self.board_drawer.highlight_square(screen, self.selected_grid_position)
            self.draw_dragged_piece(screen)

    def update(self):
        
        # if (self.board_state.is_game_over or self.board_state.num_moves_without_capture() >= 50):
        #     self.board_state.reset_board()
        #     return
        # self.self_play()
        #self.random_play()
        pass

    def random_play(self):
        move_generator = MoveGenerator()
        rand_move = move_generator.select_random_valid_move(self.board_state, self.board_state.current_player_color)
        if (rand_move is None):
            print ("No valid moves available.")
            checkmate = move_generator.is_checkmate(self.board_state.current_player_color, self.board_state)
            print ("Checkmate: ", checkmate)
            self.board_state.reset_board()
            return
        else:
            self.board_state.make_move(rand_move.start, rand_move.end)        

    def self_play(self):
        move_generator = MoveGenerator()
        best_move_tuple = self.ai.choose_best_move(self.board_state, self.board_state.current_player_color)
        print(f"Best move: {best_move_tuple}")

        if best_move_tuple[1] is None:
            print("No best move found, making random move:")
            
            rand_move = move_generator.select_random_valid_move(self.board_state, self.board_state.current_player_color)
            # If rand_move is None (no valid moves), handle that case as well
            if rand_move is not None:
                best_move_tuple = (best_move_tuple[0], ChessMove(0, rand_move.start, rand_move.end))
            else:
                print("No valid moves available.")
                return 

        self.board_state.make_move(best_move_tuple[1].start, best_move_tuple[1].end)

    def do_next_ai_move(self):
        print ("AI move")
        move_generator = MoveGenerator()
        best_move_tuple = self.ai.choose_best_move(self.board_state, self.board_state.current_player_color)
        print(f"Best move: {best_move_tuple}")

        if best_move_tuple[1] is None:
            print("No best move found, making random move:")
            
            rand_move = move_generator.select_random_valid_move(self.board_state, self.board_state.current_player_color)
            # If rand_move is None (no valid moves), handle that case as well
            if rand_move is not None:
                best_move_tuple = (best_move_tuple[0], ChessMove(0, rand_move.start, rand_move.end))
            else:
                print("No valid moves available.")
                return 

        self.board_state.make_move(best_move_tuple[1].start, best_move_tuple[1].end)

    def board_pos_to_screen_pos(self, row, col):
        """
        Convert a board position (row, col) to screen coordinates (screen_x, screen_y).
        
        Args:
            row (int): The row index on the board (0-7).
            col (int): The column index on the board (0-7).
            square_size (float): The size of a square on the board in pixels.
        
        Returns:
            tuple: A tuple containing the screen coordinates (screen_x, screen_y).
        """
        screen_x = col * self.square_size + self.square_size / 2  # Center in square
        screen_y = row * self.square_size + self.square_size / 2  # Center in square
        return screen_x, screen_y

    def draw_valid_moves(self, screen):
        if self.board_state.current_valid_moves:
            temp_surface = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
            radius = self.square_size // 4
            for move in self.board_state.current_valid_moves:
                row, col = move
                screen_x, screen_y = self.board_pos_to_screen_pos(row, col)
                pygame.draw.circle(temp_surface, self.VALID_MOVE_COLOR, (int(screen_x), int(screen_y)), radius)
            screen.blit(temp_surface, (0, 0))

    def draw_pieces_from_fen(self, screen, fen):
            placement = fen.split()[0]
            rows = placement.split('/')
            
            for j, row in enumerate(rows):
                i = 0
                for char in row:
                    if char.isdigit():
                        # Skip empty squares
                        i += int(char)
                    else:
                        piece = self.fen.get_piece_from_fen_char(char)
                        if piece:
                            x = i * self.square_size
                            y = j * self.square_size
                            self.pieceDrawer.draw_piece(screen, piece, (x, y), (self.square_size, self.square_size))
                        i += 1

       