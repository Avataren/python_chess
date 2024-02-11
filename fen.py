import numpy as np
from piece import Piece


class FEN:
    initial_board_configuration = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"
    #initial_board_configuration = "rnbqkbnr/pppp1ppp/8/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R"
    initial_castling_availability = "KQkq"
    def __init__(self):
        pass
    
    def get_piece_from_fen_char(self, char):
        """
        Returns the piece constant from the Piece class based on the FEN character.
        """
        if char.isupper():  # White pieces
            color = Piece.White
        else:  # Black pieces
            color = Piece.Black
        
        piece_type = {
            'P': Piece.Pawn,
            'N': Piece.Knight,
            'B': Piece.Bishop,
            'R': Piece.Rook,
            'Q': Piece.Queen,
            'K': Piece.King
        }.get(char.upper(), None)

        if piece_type is not None:
            return piece_type | color
        return Piece.No_Piece
    
    def get_fen_char_from_piece(self, piece: Piece):
        """
        Returns the FEN character based on the piece constant from the Piece class.
        """
        if piece == Piece.No_Piece:
            return ' '        
        
        piece_type = piece & 7  # Extract piece type
        color = piece & 8  # Extract piece color
        piece_types = {
            Piece.Pawn: 'P',
            Piece.Knight: 'N',
            Piece.Bishop: 'B',
            Piece.Rook: 'R',
            Piece.Queen: 'Q',
            Piece.King: 'K'
        }
        colors = {
            Piece.White: 'w',
            Piece.Black: 'b'
        }
        return piece_types.get(piece_type, ' ') if color == Piece.White else piece_types.get(piece_type, ' ').lower()        
    
    def fen_to_board(self, fen):
        """
        Parses the FEN string and returns the corresponding board configuration.
        """
        board = np.empty((8, 8), dtype=Piece)
        board[:] = Piece.No_Piece
        rows = fen.split('/')
        for i, row in enumerate(rows):
            col = 0
            for char in row:
                if char.isdigit():
                    col += int(char)
                else:
                    board[i, col] = self.get_piece_from_fen_char(char)
                    col += 1
        return board
    
    def board_to_fen(self, board):
        """
        Converts the board configuration to a FEN string.
        """
        fen = ''
        empty_count = 0
        for row in board:
            for piece in row:
                if piece == Piece.No_Piece:
                    empty_count += 1
                else:
                    if empty_count > 0:
                        fen += str(empty_count)
                        empty_count = 0
                    fen += self.get_fen_char_from_piece(piece)
            if empty_count > 0:
                fen += str(empty_count)
                empty_count = 0
            fen += '/'
        return fen[:-1]  # Remove the last '/'    