import pygame

class BoardDrawer:
    LIGHT_SQUARE_COLOR = "#F0D9B5"
    DARK_SQUARE_COLOR = "#B58863"
    SELECTED_SQAURE_COLOR = "#646569"
    VALID_MOVE_COLOR = "#33333333"

    def __init__(self, board_size, square_size):
        self.board_size = board_size
        self.square_size = square_size
        self.board_surface = self._init_board_surface()

    def _init_board_surface(self):
        surface = pygame.Surface((self.board_size, self.board_size))
        for i in range(8):
            for j in range(8):
                square_color = self.LIGHT_SQUARE_COLOR if (i + j) % 2 == 0 else self.DARK_SQUARE_COLOR
                pygame.draw.rect(surface, square_color, (i * self.square_size, j * self.square_size, self.square_size, self.square_size))
        return surface

    def draw_board(self, screen):
        screen.blit(self.board_surface, (0, 0))

    def highlight_square(self, screen, position):
        x, y = position
        pygame.draw.rect(screen, self.SELECTED_SQAURE_COLOR, (x * self.square_size, y * self.square_size, self.square_size, self.square_size), 4)

    def draw_valid_moves(self, screen, valid_moves):
        if not valid_moves:
            return
        
        temp_surface = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        radius = self.square_size // 8
        for move in valid_moves:
            row, col = move
            screen_x = col * self.square_size + self.square_size / 2
            screen_y = row * self.square_size + self.square_size / 2
            pygame.draw.circle(temp_surface, self.VALID_MOVE_COLOR, (int(screen_x), int(screen_y)), radius)
        screen.blit(temp_surface, (0, 0))
