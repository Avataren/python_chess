from board_evaluator import BoardEvaluator
from move_generator import MoveGenerator
from piece import Piece  # Assuming Piece class contains color definitions

class ChessAI:
    def __init__(self, max_depth):
        self.max_depth = max_depth

    def choose_best_move(self, board_state, color, depth=0, alpha=float('-inf'), beta=float('inf')):
        evaluator = BoardEvaluator()
        if depth == self.max_depth or board_state.is_game_over:
            return evaluator.evaluate(board_state, color), None
        if color == Piece.White:  # Assuming White is maximizing
            return self.maximize(board_state, color, depth, alpha, beta)
        else:  # Assuming Black is minimizing
            return self.minimize(board_state, color, depth, alpha, beta)

    def maximize(self, board_state, color, depth, alpha, beta):
        max_score = float('-inf')
        best_move = None
        for move in MoveGenerator().get_all_moves(board_state, color):
            board_state_copy = board_state.copy()
            board_state_copy.simulate_move(move.start, move.end)
            # Switch to the opponent's color for the next depth level
            opponent_color = Piece.Black if color == Piece.White else Piece.White
            score = self.choose_best_move(board_state_copy, opponent_color, depth + 1, alpha, beta)[0]

            if score > max_score:
                max_score = score
                best_move = move
            alpha = max(alpha, score)
            if beta <= alpha:
                break  # Alpha-Beta Pruning

        return max_score, best_move
    
    def minimize(self, board_state, color, depth, alpha, beta):
        min_score = float('inf')
        best_move = None
        for move in MoveGenerator().get_all_moves(board_state, color):
            board_state_copy = board_state.copy()
            board_state_copy.simulate_move(move.start, move.end)
            # Switch to the opponent's color for the next depth level
            opponent_color = Piece.Black if color == Piece.White else Piece.White
            score = self.choose_best_move(board_state_copy, opponent_color, depth + 1, alpha, beta)[0]

            if score < min_score:
                min_score = score
                best_move = move
            beta = min(beta, score)
            if beta <= alpha:
                break  # Alpha-Beta Pruning

        return min_score, best_move
