import pygame
from chess import Chess

def main():
    pygame.init()
    screen = pygame.display.set_mode((1024, 1024))
    clock = pygame.time.Clock()
    running = True

    chess = Chess(1024)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                chess.pick_up_piece(pygame.mouse.get_pos())
            elif event.type == pygame.MOUSEBUTTONUP:
                chess.move_piece(pygame.mouse.get_pos())
            elif event.type == pygame.MOUSEMOTION and chess.dragging:
                # Update the visual position of the piece being dragged
                chess.update_dragging_piece_position(pygame.mouse.get_pos())
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    chess.reset_board()

        screen.fill((55, 58, 63))
        chess.draw(screen)
        pygame.display.flip()
        clock.tick(60)  # limits FPS to 60
    pygame.quit()

if __name__ == "__main__":
    main()
