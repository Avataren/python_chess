import numpy as np
import pygame
from typing import Optional
from fen import FEN
from chess_move import ChessMove
from move_executor import MoveExecutor
from move_generator import MoveGenerator
from move_validator import MoveValidator
from piece_drawer import PieceDrawer
from piece import Piece

class Chess:
    debug = False
    board_size = 720
    square_size = board_size / 8
    LIGHT_SQUARE_COLOR = "#F0D9B5"
    DARK_SQUARE_COLOR = "#B58863"
    SELECTED_SQAURE_COLOR = "#EE5544"
    VALID_MOVE_COLOR = "#6080a0e0"
    selected_piece:Optional[Piece] = None
    selected_piece_position = None
    dragging = False    
    drag_position = None
    fen = FEN()
    current_fen_state = ""
    selected_grid_position = None
    board_surface = None
    current_valid_moves = None
    
    board = np.empty((8, 8), dtype=Piece)
    def __init__(self, board_size):
        print("Chess game initialized")
        self.board_size = board_size
        self.square_size = board_size / 8
        self.pieceDrawer = PieceDrawer("assets/pieces.png")
        self._init_board_surface()
        self.reset_board()

    def reset_board(self):
        self.current_fen_state = self.fen.initial_board_configuration
        self.board = self.fen.fen_to_board(self.current_fen_state)

    def _init_board_surface(self):
        """ Draws the static board squares onto the board surface. """
        self.board_surface = pygame.Surface((self.board_size, self.board_size))  # Step 1: Initialize board surface
        for (i, j) in [(i, j) for i in range(8) for j in range(8)]:
            square_color = self.LIGHT_SQUARE_COLOR if (i + j) % 2 == 0 else self.DARK_SQUARE_COLOR
            pygame.draw.rect(self.board_surface, square_color, (i * self.square_size, j * self.square_size, self.square_size, self.square_size))


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

    def pick_up_piece(self, mousePosition):
        if (self.dragging):
            print ("Already dragging a piece")
            return
        self.current_fen_state = self.fen.board_to_fen(self.board)
        piece = self.take_piece_at_position(mousePosition)
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
        return ( int(posX // self.square_size), int(posY // self.square_size))

    def get_piece_at_position(self, mousePosition):
        x,y = self.get_square_location_from_position(mousePosition)
        if (x < 0 or x > 7 or y < 0 or y > 7):
            return None
        return self.board[y][x]

    def take_piece_at_position(self, position):
        # Logic to get the piece at the given position
        mouseX, mouseY = position
        x = int(mouseX // self.square_size)
        y = int(mouseY // self.square_size)
        if (x < 0 or x > 7 or y < 0 or y > 7):
            self.current_valid_moves = None
            return None
        piece = self.board[y][x]
        moveGenerator = MoveGenerator(self.board)
        self.current_valid_moves = moveGenerator.get_moves_for_piece(piece, (x,y))
        print (f"valid moves:{self.current_valid_moves}")
        self.board[y][x] = Piece.No_Piece
        return piece
    
    def deselect_piece(self):
        self.selected_piece = None
        self.selected_grid_position = None
        self.dragging = False
        self.drag_position = None
        self.selected_piece_position = None
    
    def move_piece(self, mousePosition):
        # Logic to move a piece to a new position if the move is legal
        new_position = self.get_square_location_from_position(mousePosition)
        move_validator = MoveValidator(self.board)
        if self.selected_piece and move_validator.is_move_legal(self.selected_piece, self.selected_piece_position, new_position):
            # Execute the move if legal
            # Update the board state accordingly
            moveExecutor = MoveExecutor(self.board)
            moveExecutor.execute_move(self.selected_piece, new_position)
            self.current_fen_state = self.fen.board_to_fen(self.board)
            self.deselect_piece()
        else:
            print("Illegal move")
            self.selected_piece = None
            self.dragging = False
            self.drag_position = None
            self.board = self.fen.fen_to_board(self.current_fen_state)
        self.current_valid_moves = None
            
    def update_dragging_piece_position(self, mousePosition):
        self.drag_position = (mousePosition[0] - self.square_size / 2, mousePosition[1] - self.square_size / 2)
    
        square_pos = self.get_square_location_from_position(mousePosition)
        moveGenerator = MoveGenerator(self.board)
        if (self.debug):
            self.current_valid_moves = moveGenerator.get_moves_for_piece(self.selected_piece, square_pos)
        
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

        self.draw_pieces_from_fen(screen, self.fen.board_to_fen(self.board))
        #self.pieceDrawer.draw_piece(screen, Piece.BlackKnight, (0, 0), (self.square_size, self.square_size))

    def draw_valid_moves(self, screen):
        if self.current_valid_moves:
            radius = self.square_size // 4
            for (x, y) in self.current_valid_moves:  # Ensure that position unpacks into x, y coordinates
                surface_size = (radius * 2, radius * 2)
                transparent_surface = pygame.Surface(surface_size, pygame.SRCALPHA)
                # The circle's center is at (radius, radius) on the new surface
                pygame.draw.circle(transparent_surface, self.VALID_MOVE_COLOR, (radius, radius), radius)
                # Calculate the top-left corner position for blitting the surface onto the main screen
                # Adjust x, y from grid coordinates to pixel coordinates and center the circle in the square
                blit_position = (x * self.square_size + self.square_size // 4, y * self.square_size + self.square_size // 4)
                screen.blit(transparent_surface, blit_position)


                
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

       