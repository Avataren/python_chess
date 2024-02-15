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
#         board_state.make_move(move.start, move.end)    
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
    process_events()

    if depth == 0:
        return 1, 0  # Base case: return 1 move and 0 captures

    move_generator = MoveGenerator()
    num_moves = 0
    captures = 0

    moves = move_generator.generate_legal_moves(board_state).copy()

    for move in moves:
        if move.captured_piece is not Piece.No_Piece:
            captures += 1
        board_state.make_move(move)
        if chess is not None and screen is not None:
            chess.draw(screen, board_state)
            pygame.display.flip()
            time.sleep(1/10000)
        # Get the counts from the recursive call
        sub_moves, sub_captures = move_generation_test(depth - 1, board_state, chess, screen)
        num_moves += sub_moves  # Accumulate total moves
        captures += sub_captures  # Accumulate total captures
        board_state.undo_last_move()
    return num_moves, captures

def run_tests(chess = None, screen = None):
    board_state = BoardState()
    for depth in range(0, 8):
        board_state.reset_board()
        start_time = time.time()
        count, captures = move_generation_test(depth, board_state, chess, screen)
        end_time = time.time()
        print(f"Total number of moves: {count} and {captures} captures in {depth} moves in {end_time - start_time} seconds")

