from piece import Piece

class EvaluationScore:
    def __init__(self, black, white):
        self.black = black
        self.white = white
    def __str__(self):
        return f"Black: {self.black}, White: {self.white}"

    def __repr__(self):
        return f"Black: {self.black}, White: {self.white}"


class BoardEvaluator:
    
    @staticmethod 
    def evaluate(board_state):
        score = EvaluationScore(0, 0)
        for row in board_state.board:
            for piece in row:
                if piece is not Piece.No_Piece:
                    color = Piece.get_piece_color(piece)
                    points = Piece.get_piece_value(piece)
                    score.black += points if color == Piece.Black else 0
                    score.white += points if color == Piece.White else 0
        return score
