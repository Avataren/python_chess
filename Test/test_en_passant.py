import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from board_state import BoardState
from piece import Piece
from chess_move import ChessMove
from move_generator import MoveGenerator

class TestEnPassant(unittest.TestCase):

    def test_en_passant(self):
        # Set up the board state with a custom configuration
        board_state = BoardState()
        # Manually place pieces to create the scenario for en passant
        board_state.board[1][3] = Piece.BlackPawn  # Place a black pawn at (1, 3)
        board_state.board[6][3] = Piece.WhitePawn  # Place a white pawn at (6, 3)

        # List of legal moves for en passant
        moves = [
            ChessMove(Piece.WhitePawn, (6, 3), (4, 3)),  # White pawn moves from (6, 3) to (4, 3)
            ChessMove(Piece.BlackPawn, (1, 3), (2, 3)),  # Black pawn moves from (1, 3) to (2, 3)
            ChessMove(Piece.WhitePawn, (4, 3), (3, 3)),  # White pawn moves from (4, 3) to (3, 3)
            ChessMove(Piece.BlackPawn, (1, 2), (3, 2)),  # Black pawn moves from (1, 2) to (3, 2)
            ChessMove(Piece.WhitePawn, (3, 3), (2, 2))   # White pawn captures en passant at (3, 2)
        ]

        # Make the moves
        for move in moves:
            board_state.make_move(move)

        # Check that the en passant capture was performed correctly
        self.assertEqual(board_state.board[2][2], Piece.WhitePawn)  # Check that the white pawn captured en passant
        self.assertEqual(board_state.board[3][2], Piece.No_Piece)   # Check that the black pawn is no longer on the board


if __name__ == '__main__':
    unittest.main()
