import pygame
from piece import Piece

class PieceDrawer:
    
    def __init__(self, image_path):
        self.sprite_sheet = pygame.image.load(image_path).convert_alpha()

        # Assuming each piece type has equal width and each color has its own row
        self.piece_width = self.sprite_sheet.get_width() // 6
        self.piece_height = self.sprite_sheet.get_height() // 2

    def get_piece_image(self, piece_value):
        color_offset = 0 if piece_value < Piece.Black else 1

        piece_mapping = {
            Piece.Pawn: 5,
            Piece.Knight: 3,
            Piece.Bishop: 2,
            Piece.Rook: 4,
            Piece.Queen: 1,
            Piece.King: 0
        }
        piece_type = piece_value % Piece.Black
        column = piece_mapping.get(piece_type, 0)  # Default to 0 (King) if not found
        rect = pygame.Rect(column * self.piece_width, color_offset * self.piece_height, self.piece_width, self.piece_height)
        piece_image = pygame.Surface((self.piece_width, self.piece_height), pygame.SRCALPHA)
        piece_image.blit(self.sprite_sheet, (0, 0), rect)

        return piece_image


    def draw_piece(self, surface, piece_value, position, size):
        """
        Draws the specified piece on the given surface at the given position and size.
        `piece_value` should be one of the combined piece and color values from the Piece class.
        Position is a tuple (x, y), and size is the desired size to scale the piece to.
        """
        piece_image = self.get_piece_image(piece_value)
        piece_image = pygame.transform.smoothscale(piece_image, size)  # Use smoothscale here
        surface.blit(piece_image, position)
