import numpy as np
from piece import Piece


class FEN:
    """
    (From wikipedia)
    A FEN record defines a particular game position, all in one text line and using only the ASCII character set. A text file with only FEN data records should use the filename extension .fen.[4]

    A FEN record contains six fields, each separated by a space. The fields are as follows:[5]

    1   Piece placement data: Each rank is described, starting with rank 8 and ending with rank 1, with a "/" between each one; 
        within each rank, the contents of the squares are described in order from the a-file to the h-file. 
        Each piece is identified by a single letter taken from the standard English names in algebraic notation
        (pawn = "P", knight = "N", bishop = "B", rook = "R", queen = "Q" and king = "K"). 
        White pieces are designated using uppercase letters ("PNBRQK"), while black pieces use lowercase letters ("pnbrqk"). 
        A set of one or more consecutive empty squares within a rank is denoted by a digit from "1" to "8", corresponding to the number of squares.

    2   Active color: "w" means that White is to move; "b" means that Black is to move.

    3   Castling availability: If neither side has the ability to castle, this field uses the character "-". Otherwise, 
        this field contains one or more letters: "K" if White can castle kingside, "Q" if White can castle queenside, 
        "k" if Black can castle kingside, and "q" if Black can castle queenside. 
        A situation that temporarily prevents castling does not prevent the use of this notation.

    4   En passant target square: This is a square over which a pawn has just passed while moving two squares; it is given in algebraic notation. 
        If there is no en passant target square, this field uses the character "-". 
        This is recorded regardless of whether there is a pawn in position to capture en passant.
        An updated version of the spec has since made it so the target square is recorded only if a legal en passant capture is possible, 
        but the old version of the standard is the one most commonly used.

    5   Halfmove clock: The number of halfmoves since the last capture or pawn advance, used for the fifty-move rule.

    6   Fullmove number: The number of the full moves. It starts at 1 and is incremented after Black's move.    
    """

    standard_game = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    fen_position_2 = "r3k2r/p1ppqpb1/bn2pnp1/3PN3/1p2P3/2N2Q1p/PPPBBPPP/R3K2R w KQkq - "
    fen_position_3 = "8/2p5/3p4/KP5r/1R3p1k/8/4P1P1/8 w - - "
    fen_position_4 = "r3k2r/Pppp1ppp/1b3nbN/nP6/BBP1P3/q4N2/Pp1P2PP/R2Q1RK1 w kq - 0 1"
    fen_position_5 = "rnbq1k1r/pp1Pbppp/2p5/8/2B5/8/PPP1NnPP/RNBQK2R w KQ - 1 8"
    fen_position_6 = "r4rk1/1pp1qppp/p1np1n2/2b1p1B1/2B1P1b1/P1NP1N2/1PP1QPPP/R4RK1 w - - 0 10"
    #"rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"
    initial_board_configuration = standard_game
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
    
    def fen_to_board_state(self, fen, board_state):
        """
        Parses the FEN string and updates the corresponding board configuration, 
        castling availability, active color, en passant target, halfmove clock, and fullmove counter.
        """
        parts = fen.split(' ')
        while len(parts) < 6:
            if len(parts) == 1:
                parts.extend(['w', '-', '-', '0', '1'])  # Default values for missing parts
            else:
                parts.append('-')

        board_config, active_color, castling_avail, en_passant, halfmove_clock, fullmove_number = parts[0:6]

        # Parse board configuration
        board = board_state.board
        board[:] = Piece.No_Piece
        rows = board_config.split('/')
        for i, row in enumerate(rows):
            col = 0
            for char in row:
                if char.isdigit():
                    col += int(char)
                else:
                    board[i, col] = self.get_piece_from_fen_char(char)
                    col += 1

        # Parse active color
        board_state.current_player_color = Piece.White if active_color == 'w' else Piece.Black

        # Reset castling availability
        board_state.has_moved = {key: True for key in board_state.has_moved}

        # Update castling availability based on FEN
        if 'K' in castling_avail:
            board_state.has_moved['KR'] = False
            board_state.has_moved['K'] = False
        if 'Q' in castling_avail:
            board_state.has_moved['QR'] = False
            board_state.has_moved['K'] = False
        if 'k' in castling_avail:
            board_state.has_moved['kr'] = False
            board_state.has_moved['k'] = False
        if 'q' in castling_avail:
            board_state.has_moved['qr'] = False
            board_state.has_moved['k'] = False

        # Validate king and rook positions if no castling rights are supplied
        # self.validate_king_rook_positions_for_castling(board, board_state, castling_avail)

        # Parse en passant target square
        # You need to handle this based on your board state structure
        # For now, it's just acknowledged and not utilized
        # board_state.en_passant_target = en_passant

        # Parse halfmove clock and fullmove number
        board_state.halfmove_clock = int(halfmove_clock)
        board_state.move_number[Piece.White] = int(fullmove_number) - 1
        board_state.move_number[Piece.Black] = int(fullmove_number) - 1

    # def validate_king_rook_positions_for_castling(self, board, board_state, castling_avail):
    #     """
    #     Validates the positions of kings and rooks to determine if castling rights should be adjusted.
    #     """
    #     # Standard starting positions for kings and rooks
    #     standard_positions = {
    #         'K': (7, 4), 'KR': (7, 7), 'QR': (7, 0),
    #         'k': (0, 4), 'kr': (0, 7), 'qr': (0, 0)
    #     }

    #     for piece, position in standard_positions.items():
    #         if piece in castling_avail:  # Skip if castling right is explicitly given
    #             continue

    #         # Check if the piece is not in its standard position
    #         if board[position[0]][position[1]] != self.get_piece_from_fen_char(piece.upper()):
    #             board_state.has_moved[piece] = True  # Mark as moved
    #             print ("Adjusting castling rights for ", piece,"at position", position, " as it is not in standard position")


    def board_state_to_fen(self, board_state):
        # Piece placement
        board = board_state.board
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
        fen = fen[:-1]  # Remove the last '/'
        
        # Active color
        if board_state.current_player_color == Piece.White:
            fen += ' w'
        else:
            fen += ' b'
        
        # Castling availability
        castling = ''
        castling += 'K' if board_state.has_moved['K'] == False else ''
        castling += 'Q' if board_state.has_moved['Q'] == False else ''
        castling += 'k' if board_state.has_moved['k'] == False else ''
        castling += 'q' if board_state.has_moved['q'] == False else ''
        fen += ' ' + castling if castling else ' -'
        
        # En passant target square
        # Assuming you have a way to determine the en passant square, otherwise put '-'
        fen += ' -'  # Replace this with your logic to determine the en passant square
        
        # Halfmove clock
        # Assuming you have a way to keep track of this, otherwise put '0'
        fen += ' 0'  # Replace this with your actual halfmove clock
        
        # Fullmove number
        # Assuming the move_number is incremented after each move and starts at 1
        fullmove_number = max(board_state.move_number[Piece.White], board_state.move_number[Piece.Black]) + 1
        fen += f' {fullmove_number}'
        
        return fen
