import time
import pygame
from board_state import BoardState
from fen import FEN
from move_generator import MoveGenerator
from piece import Piece

def wait_for_keypress():
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                waiting = False

def process_events(board_state):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
            
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                fen = FEN()
                fen = fen.board_state_to_fen(board_state)
                file = open("fen.txt", "w")
                file.write(fen)
                file.close()                
         
            

def move_generation_test(depth, board_state, chess, screen):
    process_events(board_state)
    if depth == 0:
        return 1, 0, 0  # Base case: return 1 move and 0 captures

    move_generator = MoveGenerator()
    num_moves = 0
    captures = 0
    castlings = 0
    
    moves = move_generator.generate_legal_moves(board_state).copy()

    for move in moves:

            
        #print ("making move: ", move)
        board_state.make_move(move)

        hist_move = board_state.move_history[-1][0]

        if hist_move.captured_piece is not Piece.No_Piece:
            captures += 1
        if hist_move.is_castling_move:
            castlings += 1

        if chess is not None and screen is not None:
            chess.draw(screen, board_state)
            pygame.display.flip()
            #wait_for_keypress()
            time.sleep(0)
        # Get the counts from the recursive call
        sub_moves, sub_captures, sub_castlings = move_generation_test(depth - 1, board_state, chess, screen)
        num_moves += sub_moves  # Accumulate total moves
        captures += sub_captures  # Accumulate total captures
        # if (captures > 1576):
        #         board_state.save()
        #         exit()
                
        castlings += sub_castlings
        board_state.undo_last_move()
        
    return num_moves, captures, castlings

def run_tests(chess = None, screen = None):
    board_state = BoardState()
    for depth in range(0, 8):
        board_state.reset_board()
        start_time = time.time()
        count, captures, castlings = move_generation_test(depth, board_state, chess, screen)
        end_time = time.time()
        print(f"depth: {depth}, moves: {count}, {captures} captures, castlings: {castlings} in {end_time - start_time} seconds")

