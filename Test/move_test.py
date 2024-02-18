import os
import sys
import unittest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import time
import pygame
from board_state import BoardState
from chess_move import ChessMove
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
         
            
test_history = []

def move_generation_test(depth, board_state, chess, screen):
    process_events(board_state)
    if depth == 0:
        return 1, 0, 0, 0  # Base case: return 1 move and 0 captures

    move_generator = MoveGenerator()
    num_moves = 0
    captures = 0
    castlings = 0
    en_passants = 0
    moves = move_generator.generate_legal_moves(board_state)

    for move in moves:

        #print ("making move: ", move)
        board_state.make_move(move)
        #fen = FEN()
        #print(fen.board_state_to_fen(board_state))
        hist_move = board_state.move_history[-1][0]

        test_history.append((hist_move, board_state.has_moved.copy()))

        if hist_move.captured_piece is not Piece.No_Piece:
            captures += 1
        if hist_move.is_castling_move:
            castlings += 1
        if hist_move.is_en_passant:
            en_passants += 1
            
        if chess is not None and screen is not None:
            chess.draw(screen, board_state)
            pygame.display.flip()
            #wait_for_keypress()
            time.sleep(1/2)
        # Get the counts from the recursive call
        sub_moves, sub_captures, sub_castlings, sub_ep = move_generation_test(depth - 1, board_state, chess, screen)
        num_moves += sub_moves  # Accumulate total moves
        captures += sub_captures  # Accumulate total captures
        en_passants += sub_ep
        # if (en_passants > 0):
        #         board_state.save(test_history)
        #         exit()
                
        castlings += sub_castlings
        board_state.undo_last_move()
        
    return num_moves, captures, castlings, en_passants

move_generator = MoveGenerator()

# def Perft(depth, board_state):
    
#     nodes = 0
#     if (depth == 0):
#         return 1
#     move_list = move_generator.generate_legal_moves(board_state).copy()
#     n_moves = len(move_list)
#     for i in range(n_moves):
#         board_state.make_move(move_list[i])
#         nodes += Perft(depth - 1, board_state)
#         board_state.undo_last_move()
#     return nodes

def Perft(depth, board_state, move_counts=None, current_depth=0):
    if move_counts is None:
        move_counts = {d: {} for d in range(current_depth, depth + 1)}

    nodes = 0
    if depth == 0:
        return 1, move_counts  # Ensure to return a tuple here

    move_list = move_generator.generate_legal_moves(board_state).copy()

    for move in move_list:
        piece = board_state.board[move.start[0]][move.start[1]]
        #print (Piece.is_knight(piece))
        #print (piece == Piece.WhiteKnight)
        chess_move = ChessMove(piece, move.start, move.end, board_state.board[move.end[0]][move.end[1]], move.end)
        board_state.make_move(chess_move)
        move_key_from = ChessMove.to_chess_notation(move.start[0], move.start[1])
        move_key_to = ChessMove.to_chess_notation(move.end[0], move.end[1])
        move_key = move_key_from + move_key_to
        #if (piece == Piece.WhiteKnight):
        #    move_key = "N" + move_key
        #if (piece == Piece.BlackKnight):
        #    move_key = "n" + move_key
        #move_key = Piece.description(piece) + " to " + move_key
        # Update move counts for the current depth
        if move_counts.get(current_depth) is not None:
            move_counts[current_depth][move_key] = move_counts[current_depth].get(move_key, 0) + 1
    
        sub_nodes, sub_move_counts = Perft(depth - 1, board_state, move_counts, current_depth + 1)
        nodes += sub_nodes
        board_state.undo_last_move()

    if current_depth == 0:
        # At the top level, return the entire move counts structure along with the total node count
        return nodes, move_counts

    return nodes, move_counts  # Make sure to return move_counts here as well
class TestPerft(unittest.TestCase):

    def setUp(self) -> None:
        return super().setUp()
    
    def test_perft(self):
        print ("Running perft tests, please wait...")
        node_counts = [20, 400, 8902, 197281, 4865609, 119060324, 3195901860, 84998978956]
        depth = 4
        board_state = BoardState()
        start_time = time.time()
        nodes, move_counts = Perft(depth, board_state)
        end_time = time.time()
        print(f"depth: {depth}, nodes: {nodes} in {end_time - start_time} seconds")
        
        for visualizedepth in range(1, depth):
            curr_count = move_counts.get(visualizedepth)
            total_nodes = 0
            for key in curr_count:
                total_nodes+= curr_count[key]
                
            if curr_count is not None:
                sorted_keys = sorted(curr_count)
                sorted_move_counts = {key: curr_count[key] for key in sorted_keys}  # Use curr_count here
                #print( visualizedepth , f"({total_nodes}) : " , sorted_move_counts)
                print ("Depth ", visualizedepth, ":", total_nodes)
                for (key, value) in sorted_move_counts.items():
                    print (key, ":", value)
            else:
                print("No moves recorded for depth", depth-1)
            print ("-----------------------------------")        
        



def run_tests(chess = None, screen = None):
    pass
    # board_state = BoardState()
    # #for depth in range (0,8):
    # depth = 2
    
    # start_time = time.time()
    # nodes, move_counts = Perft(depth, board_state)
    # end_time = time.time()
    # print(f"depth: {depth}, nodes: {nodes} in {end_time - start_time} seconds")
    # for visualizedepth in range(1, depth):
    #     curr_count = move_counts.get(visualizedepth)
    #     if curr_count is not None:
    #         sorted_keys = sorted(curr_count)
    #         sorted_move_counts = {key: curr_count[key] for key in sorted_keys}  # Use curr_count here
    #         print( visualizedepth , " : " , sorted_move_counts)
    #     else:
    #         print("No moves recorded for depth", depth-1)
    #     print ("-----------------------------------")
        
#        print(sorted(move_counts.get(depth-1)))
    
#     for depth in range(0, 8):
# #        board_state.reset_board()
#         start_time = time.time()
#         count, captures, castlings, ep = move_generation_test(depth, board_state, chess, screen)
#         end_time = time.time()
#         print(f"depth: {depth}, moves: {count}, {captures} captures, castlings: {castlings}, ep: {ep} in {end_time - start_time} seconds")
#     print ("Test complete!")

if __name__ == '__main__':
    unittest.main()