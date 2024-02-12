import pygame
from typing import Optional
from board_state import BoardState
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
    
    def __init__(self, board_size):
        print("Chess game initialized")
        self.board_size = board_size
        self.square_size = board_size / 8
        self.pieceDrawer = PieceDrawer("assets/pieces.png")
        self._init_board_surface()
        self.reset_board()

    def reset_board(self):
        self.board_state.reset_board()

    def _init_board_surface(self):
        """ Draws the static board squares onto the board surface. """
        self.board_surface = pygame.Surface((self.board_size, self.board_size))  # Step 1: Initialize board surface
        for (i, j) in [(i, j) for i in range(8) for j in range(8)]:
            square_color = self.LIGHT_SQUARE_COLOR if (i + j) % 2 == 0 else self.DARK_SQUARE_COLOR
            pygame.draw.rect(self.board_surface, square_color, (i * self.square_size, j * self.square_size, self.square_size, self.square_size))


    def pick_up_piece(self, mousePosition):
        if (self.dragging):
            print ("Already dragging a piece")
            return
        piece = self.board_state.take_piece_at_position(mousePosition, self.square_size)
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
        # Logic to move a piece to a new position if the move is legal
        new_position = self.get_square_location_from_position(mousePosition)
        old_position = self.board_state.selected_piece_position
        if self.selected_piece and self.board_state.is_move_legal(new_position):
            print ("Executing move!")
            self.board_state.execute_move(self.selected_piece, old_position, new_position)
            self.deselect_piece()
        else:
            print("Illegal move")
            row, col = self.board_state.selected_piece_position
            self.board_state.board[row][col] = self.selected_piece
            self.selected_piece = None
            self.dragging = False
            self.drag_position = None
        self.board_state.current_valid_moves = None
            
    def update_dragging_piece_position(self, mousePosition):
        self.drag_position = (mousePosition[0] - self.square_size / 2, mousePosition[1] - self.square_size / 2)
    
        col,row = self.get_square_location_from_position(mousePosition)
        moveGenerator = MoveGenerator()
        if (self.debug):
            self.board_state.current_valid_moves = moveGenerator.get_moves_for_piece(self.selected_piece, (row, col), self.board_state.board)
        
    def draw_dragged_piece(self, screen):
        if self.drag_position is not None and self.selected_piece is not None:
            self.pieceDrawer.draw_piece(screen, self.selected_piece, self.drag_position, (self.square_size, self.square_size))
    
    def draw(self, screen):
        self.draw_board(screen)
        
        if (self.dragging):
            self.draw_dragged_piece(screen)
    
    def draw_board(self, screen):
        screen.blit(self.board_surface, (0, 0))
        if self.selected_grid_position is not None:
            x,y= self.selected_grid_position
            pygame.draw.rect(screen, self.SELECTED_SQAURE_COLOR, (x * self.square_size, y * self.square_size, self.square_size, self.square_size), 4)
            self.draw_valid_moves(screen)

        self.draw_pieces_from_fen(screen, self.fen.board_to_fen(self.board_state.board))
        #self.pieceDrawer.draw_piece(screen, Piece.BlackKnight, (0, 0), (self.square_size, self.square_size))

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
            # Create a temporary surface with per-pixel alpha capabilities
            temp_surface = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
            radius = self.square_size // 4
            
            for move in self.board_state.current_valid_moves:
                row, col = move
                screen_x, screen_y = self.board_pos_to_screen_pos(row, col)
                
                # Draw a circle on the temporary surface instead of the main screen
                pygame.draw.circle(temp_surface, self.VALID_MOVE_COLOR, (int(screen_x), int(screen_y)), radius)
            
            # Blit the temporary surface onto the main screen surface
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

       