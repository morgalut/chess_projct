# board.py
from board.model.bishop import Bishop
from board.model.king import King
from board.model.knight import Knight
from board.model.pawn import Pawn
from board.model.queen import Queen
from board.model.rook import Rook
from collections import defaultdict

class Board:
    def __init__(self):
        self.board = [[None for _ in range(8)] for _ in range(8)]
        self.position_history = defaultdict(int)  # Tracks occurrences of each board position
        self.no_capture_or_pawn_move_count = 0  # Tracks moves since the last capture or pawn move
        self.setup_pieces()

    def setup_pieces(self):
        # Placing pieces in the standard initial positions
        # Place the Rooks
        self.place_piece(Rook, 'white', 0, 0)
        self.place_piece(Rook, 'white', 7, 0)
        self.place_piece(Rook, 'black', 0, 7)
        self.place_piece(Rook, 'black', 7, 7)
        # Place the Knights
        self.place_piece(Knight, 'white', 1, 0)
        self.place_piece(Knight, 'white', 6, 0)
        self.place_piece(Knight, 'black', 1, 7)
        self.place_piece(Knight, 'black', 6, 7)
        # Place the Bishops
        self.place_piece(Bishop, 'white', 2, 0)
        self.place_piece(Bishop, 'white', 5, 0)
        self.place_piece(Bishop, 'black', 2, 7)
        self.place_piece(Bishop, 'black', 5, 7)
        # Place the Queens
        self.place_piece(Queen, 'white', 3, 0)
        self.place_piece(Queen, 'black', 3, 7)
        # Place the Kings
        self.place_piece(King, 'white', 4, 0)
        self.place_piece(King, 'black', 4, 7)
        # Place the Pawns
        for i in range(8):
            self.place_piece(Pawn, 'white', i, 1)
            self.place_piece(Pawn, 'black', i, 6)


    def place_piece(self, piece_type, color, x, y):
        if self.is_within_bounds(x, y):
            # Instantiate the piece with position parameters
            piece = piece_type(color, x, y)
            self.board[y][x] = piece


    def get_piece(self, x, y):
        return self.board[y][x] if self.is_within_bounds(x, y) else None

    def is_empty(self, x, y):
        empty = self.is_within_bounds(x, y) and self.get_piece(x, y) is None
        print(f"Checking if position ({x}, {y}) is empty: {empty}")
        return empty


    def is_opponent_piece(self, x, y, color):
        if not self.is_within_bounds(x, y):
            print(f"Position ({x}, {y}) is out of bounds.")
            return False
        piece = self.get_piece(x, y)
        opponent = piece is not None and piece.color != color
        print(f"Checking if piece at ({x}, {y}) is an opponent piece: {opponent}")
        return opponent

    def move_piece(self, start_pos, end_pos):
        """Move a piece from start_pos to end_pos if the move is legal."""
        start_x, start_y = self.pos_to_index(start_pos)
        end_x, end_y = self.pos_to_index(end_pos)
        moving_piece = self.get_piece(start_x, start_y)
        if moving_piece and self.is_legal_move(start_pos, end_pos, moving_piece.color):
            self.board[end_y][end_x] = self.board[start_y][start_x]
            self.board[start_y][start_x] = None
            self.update_position_history()
            return True
        return False



    def is_legal_move(self, start_pos, end_pos, color):
        start_x, start_y = self.pos_to_index(start_pos)
        end_x, end_y = self.pos_to_index(end_pos)
        moving_piece = self.get_piece(start_x, start_y)
        
        if not moving_piece or moving_piece.color != color:
            return False
        
        if not moving_piece.is_valid_move(start_x, start_y, end_x, end_y, self):
            return False

        # Temporarily make the move
        captured_piece = self.board[end_y][end_x]  # Capture the piece that might be at the end position
        self.board[end_y][end_x] = moving_piece
        self.board[start_y][start_x] = None
        
        # Check for check condition
        king_pos = self.find_king(color)
        in_check = self.is_king_in_check(king_pos, color)
        
        # Undo the move
        self.board[start_y][start_x] = moving_piece
        self.board[end_y][end_x] = captured_piece
        
        return not in_check


    def update_position_history(self):
        self.position_history[self.current_position()] += 1

    def current_position(self):
        return ''.join(str(self.board[y][x]) for y in range(8) for x in range(8))

    def find_king(self, color):
        for y in range(8):
            for x in range(8):
                piece = self.get_piece(x, y)
                if isinstance(piece, King) and piece.color == color:
                    return (x, y)
        return None

    def is_king_in_check(self, king_pos, color):
        opponent_color = 'black' if color == 'white' else 'white'
        x_king, y_king = king_pos
        for y in range(8):
            for x in range(8):
                piece = self.get_piece(x, y)
                if piece and piece.color == opponent_color:
                    if (x_king, y_king) in piece.get_legal_moves(x, y, self):
                        return True
        return False


    def pos_to_index(self, pos):
        if isinstance(pos, tuple):
            x, y = pos
        else:
            column, row = pos[0], pos[1]
            x = ord(column) - ord('a')
            y = int(row) - 1
        
        if not (0 <= x < 8 and 0 <= y < 8):
            raise ValueError(f"Invalid position: {pos}")
        return (x, y)


    def is_within_bounds(self, x, y):
        return 0 <= x < 8 and 0 <= y < 8

    def get_all_pieces(self, color=None):
        return [p for row in self.board for p in row if p and (color is None or p.color == color)]


    def can_move_piece(self, x, y):
        """Check if the piece at position (x, y) can make any legal moves."""
        piece = self.get_piece(x, y)
        if not piece:
            return False

        # Assume a theoretical maximum board movement range for simplicity
        for dx in range(-8, 9):
            for dy in range(-8, 9):
                nx, ny = x + dx, y + dy
                if 0 <= nx < 8 and 0 <= ny < 8:  # Check bounds
                    if self.is_legal_move((x, y), (nx, ny), piece.color):
                        return True
        return False
    
    def get_board_state(self):
        """Retrieve the current state of the chess board."""
        state = []
        for row in self.board:
            row_state = []
            for piece in row:
                if piece is None:
                    row_state.append(None)
                else:
                    row_state.append({
                        'type': type(piece).__name__,
                        'color': piece.color
                    })
            state.append(row_state)
        return state