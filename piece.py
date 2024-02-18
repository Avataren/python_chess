from enum import IntEnum

class Piece(IntEnum):
    No_Piece = 0
    Pawn = 1
    Knight = 2
    Bishop = 3
    Rook = 4
    Queen = 5
    King = 6

    # Piece Colors
    White = 0
    Black = 8

    WhitePawn = Pawn | White  # 1
    WhiteKnight = Knight | White  # 2
    WhiteBishop = Bishop | White  # 3
    WhiteRook = Rook | White  # 4
    WhiteQueen = Queen | White  # 5
    WhiteKing = King | White  # 6

    BlackPawn = Pawn | Black  # 9
    BlackKnight = Knight | Black  # 10
    BlackBishop = Bishop | Black  # 11
    BlackRook = Rook | Black  # 12
    BlackQueen = Queen | Black  # 13
    BlackKing = King | Black  # 14

    MaxPieceIndex = BlackKing

    @staticmethod
    def is_pawn(piece):
        return piece & 7 == Piece.Pawn

    @staticmethod
    def is_knight(piece):
        return piece & 7 == Piece.Knight

    @staticmethod
    def is_bishop(piece):
        return piece & 7 == Piece.Bishop

    @staticmethod
    def is_rook(piece):
        return piece & 7 == Piece.Rook

    @staticmethod
    def is_queen(piece):
        return piece & 7 == Piece.Queen

    @staticmethod
    def is_king(piece):
        return piece & 7 == Piece.King

    @staticmethod
    def is_black_king(piece):
        return piece & 7 == Piece.King and piece >= Piece.BlackKing

    @staticmethod
    def is_white_king(piece):
        return piece == Piece.WhiteKing

    @staticmethod
    def get_piece_color(piece):
        if piece >= Piece.Black:
            return Piece.Black
        else:
            return Piece.White

    @staticmethod
    def get_opposite_color(piece):
        if piece >= Piece.Black:
            return Piece.White
        else:
            return Piece.Black

    @staticmethod
    def get_piece_value(piece):
        piece_type = piece & 7
        if piece_type == Piece.Pawn:
            return 1
        if piece_type == Piece.Knight:
            return 3
        if piece_type == Piece.Bishop:
            return 3
        if piece_type == Piece.Rook:
            return 5
        if piece_type == Piece.Queen:
            return 9
        if piece_type == Piece.King:
            return 1000

    @staticmethod
    def description(piece):
        pieceType = (
            "Pawn"
            if Piece.is_pawn(piece)
            else "Knight"
            if Piece.is_knight(piece)
            else "Bishop"
            if Piece.is_bishop(piece)
            else "Rook"
            if Piece.is_rook(piece)
            else "Queen"
            if Piece.is_queen(piece)
            else "King"
            if Piece.is_king(piece)
            else "No Piece"
        )
        color = "White"
        if piece >= Piece.Black:
            color = "Black"
      
        return color + " " + pieceType        

    def __str__(self):
        return self.description()
