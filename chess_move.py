class ChessMove:
    def __init__(self, piece, start, end):
        self.piece = piece
        self.start = start
        self.end = end

    def __str__(self):
        return f"Move {self.piece} from {self.start} to {self.end}"

    def __repr__(self):
        return f"Move {self.piece} from {self.start} to {self.end}"