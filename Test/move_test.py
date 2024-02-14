import time
import pygame
from board_state import BoardState
from move_generator import MoveGenerator
from piece import Piece

# def move_generation_test(depth, board_state):
#     if depth == 0:
#         return 1, 0  # Base case: return 1 move and 0 captures
#     move_generator = MoveGenerator()
#     num_moves = 0
#     captures = 0
#     moves = move_generator.get_first_of_all_moves(board_state)
#     for move in moves:
#         if move.captured_piece is not Piece.No_Piece:
#             captures += 1
#         board_state.move_piece(move.start, move.end)    
#         # Get the counts from the recursive call
#         sub_moves, sub_captures = move_generation_test(depth - 1, board_state)
#         num_moves += sub_moves  # Accumulate total moves
#         captures += sub_captures  # Accumulate total captures
#         board_state.undo_last_move()
#     return num_moves, captures

def process_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

def move_generation_test(depth, board_state, chess, screen):
    global closk
    if depth == 0:
        return 1, 0  # Base case: return 1 move and 0 captures
    move_generator = MoveGenerator()
    num_moves = 0
    captures = 0
    moves = move_generator.get_first_of_all_moves(board_state)
    for move in moves:
        if move.captured_piece is not Piece.No_Piece:
            captures += 1
        board_state.move_piece(move.start, move.end)
        if (chess is not None and screen is not None):
            chess.draw(screen, board_state)
            process_events()
            pygame.display.flip()
            time.sleep(0.01)
        # Get the counts from the recursive call
        sub_moves, sub_captures = move_generation_test(depth - 1, board_state, chess, screen)
        num_moves += sub_moves  # Accumulate total moves
        captures += sub_captures  # Accumulate total captures
        board_state.undo_last_move()
    return num_moves, captures

def run_tests(chess, screen):
    board_state = BoardState()
    board_state.reset_board()
    for depth in range(0, 7):
        start_time = time.time()
        count, captures = move_generation_test(depth, board_state, chess, screen)
        end_time = time.time()
        print(f"Total number of moves: {count} and {captures} captures in {depth} moves in {end_time - start_time} seconds")

