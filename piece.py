class Piece:
    # Piece Types
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

    WhitePawn = Pawn | White; # 1
    WhiteKnight = Knight | White; # 2
    WhiteBishop = Bishop | White; # 3
    WhiteRook = Rook | White; # 4
    WhiteQueen = Queen | White; # 5
    WhiteKing = King | White; # 6

    BlackPawn = Pawn | Black; # 9
    BlackKnight = Knight | Black; # 10
    BlackBishop = Bishop | Black; # 11
    BlackRook = Rook | Black; # 12
    BlackQueen = Queen | Black; # 13
    BlackKing = King | Black; # 14

    MaxPieceIndex = BlackKing

    PieceIndices = {
        WhitePawn, WhiteKnight, WhiteBishop, WhiteRook, WhiteQueen, WhiteKing,
        BlackPawn, BlackKnight, BlackBishop, BlackRook, BlackQueen, BlackKing
    }