from typing import Optional
from piece import Piece

class MoveExecutor:
    def __init__(self, board_state):
        self.board_state = board_state  # A 2D array representing the board

    def execute_move(self, piece:Optional[Piece], new_position):
        self.board_state[new_position[1]][new_position[0]] = piece
        return True
        