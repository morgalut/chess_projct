"""
This module defines the Board class which manages the chess board state, including
the placement of pieces, determining legal moves, and handling move operations.
"""
from board.model.bishop import Bishop
from board.model.king import King
from board.model.knight import Knight
from board.model.pawn import Pawn
from board.model.queen import Queen
from board.model.rook import Rook
from collections import defaultdict

class Board:
    """Represents the chess board, handling initialization, piece placement, and move validation."""
    
    def __init__(self):
        """Initialize an empty board and setup the pieces."""
        self.board = [[None for _ in range(8)] for _ in range(8)]
        self.position_history = defaultdict(int)  # Tracks occurrences of each board position
        self.no_capture_or_pawn_move_count = 0  # Tracks moves since the last capture or pawn move
        self.setup_pieces()

    def setup_pieces(self):
        """Setup pieces on the board in their initial positions."""
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
        """Place a piece of type piece_type and color at position (x, y)."""
        if self.is_within_bounds(x, y):
            # Instantiate the piece with position parameters
            piece = piece_type(color, x, y)
            self.board[y][x] = piece


    def get_piece(self, x, y):
        """Return the piece at the given board position (x, y)."""
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
        """Move a piece from start_pos to end_pos if the move is legal, including handling castling."""
        start_x, start_y = self.pos_to_index(start_pos)
        end_x, end_y = self.pos_to_index(end_pos)
        moving_piece = self.get_piece(start_x, start_y)
        
        if not moving_piece:
            return False  # No piece at the starting position

        # Check if the move is a castling move
        if isinstance(moving_piece, King) and abs(start_y - end_y) == 2 and not moving_piece.has_moved:
            if self.can_castle(moving_piece, start_x, start_y, end_y):
                return self.perform_castling(moving_piece, start_x, start_y, end_y)

        # Perform a regular move if not castling
        if self.is_legal_move(start_pos, end_pos, moving_piece.color):
            self.board[end_y][end_x] = moving_piece
            self.board[start_y][start_x] = None
            moving_piece.has_moved = True  # Mark the piece as having moved
            self.update_position_history()  # Keep track of the board's state
            return True
        
        return False

    def can_castle(self, king, start_x, start_y, end_y):
        """Check if castling is possible given the king's current state and position."""
        direction = 1 if end_y > start_y else -1
        rook_pos_y = start_y + (direction * 4) if direction == 1 else 0  # Rook's initial position
        steps = range(start_y + direction, rook_pos_y, direction)
        
        if any(self.board[start_x][y] for y in steps):  # Ensure path is clear
            return False
        if any(self.is_square_under_attack(start_x, y, king.color) for y in steps):  # Ensure path is not under attack
            return False

        rook = self.get_piece(start_x, rook_pos_y)
        return isinstance(rook, Rook) and not rook.has_moved

    def perform_castling(self, king, start_x, start_y, end_y):
        """Execute the castling move, moving both the king and the rook."""
        direction = 1 if end_y > start_y else -1
        rook_start_y = start_y + (direction * 4) if direction == 1 else 0
        rook_end_y = start_y + direction  # Where the rook ends up after castling

        # Move the rook
        rook = self.get_piece(start_x, rook_start_y)
        self.board[start_x][rook_end_y] = rook
        self.board[start_x][rook_start_y] = None

        # Move the king
        king_end_y = start_y + (2 * direction)
        self.board[start_x][king_end_y] = king
        self.board[start_x][start_y] = None
        
        king.has_moved = True
        rook.has_moved = True
        self.update_position_history()
        return True



    def is_legal_move(self, start_pos, end_pos, color):
        start_x, start_y = self.pos_to_index(start_pos)
        end_x, end_y = self.pos_to_index(end_pos)
        moving_piece = self.get_piece(start_x, start_y)
        
        if not moving_piece or moving_piece.color != color:
            return False
        
        if not moving_piece.is_valid_move(start_x, start_y, end_x, end_y, self):
            return False

        # Temporarily make the move
        captured_piece = self.board[end_y][end_x]
        self.board[end_y][end_x] = moving_piece
        self.board[start_y][start_x] = None
        
        # Check for check condition
        in_check = self.is_king_in_check(color)  # Corrected to only pass color
        
        # Undo the move
        self.board[start_y][start_x] = moving_piece
        self.board[end_y][end_x] = captured_piece
        
        return not in_check



    def update_position_history(self):
        self.position_history[self.current_position()] += 1

    def current_position(self):
        return ''.join(str(self.board[y][x]) for y in range(8) for x in range(8))


    def is_in_check(self, color):
        """Check if the king of the given color is in check."""
        king_pos = self.find_king(color)
        if king_pos:
            return self.is_king_in_check(king_pos, color)
        return False

    def is_king_in_check(self, color):
        """Check if the king of the given color is under attack."""
        king_pos = self.find_king(color)
        if king_pos:
            return self._is_position_under_attack(king_pos, color)
        return False


    def find_king(self, color):
        """Find the king of the specified color on the board."""
        for y in range(8):
            for x in range(8):
                piece = self.get_piece(x, y)
                if isinstance(piece, King) and piece.color == color:
                    return (x, y)
        raise ValueError(f"No king found for color {color}")

    def _is_position_under_attack(self, pos, color):
        x, y = pos
        opponent_color = 'white' if color == 'black' else 'black'
        for j in range(8):
            for i in range(8):
                piece = self.get_piece(i, j)
                if piece and piece.color == opponent_color:
                    # Pass False to avoid checking castling moves during attack checks
                    if (x, y) in piece.get_legal_moves(i, j, self, check_castling=False):
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
        """Check if (x, y) is within the board boundaries."""
        return 0 <= x < 8 and 0 <= y < 8

    def get_all_pieces(self, color):
        return [self.board[i][j] for i in range(8) for j in range(8) if self.board[i][j] and self.board[i][j].color == color]



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
    
    def is_square_under_attack(self, x, y, color):
        # Assuming 'opposite_color' is a function or a way to get the opposite color
        opposite_color = 'white' if color == 'black' else 'black'
        opponent_pieces = self.get_all_pieces(opposite_color)  # This should retrieve all pieces of the opponent
        
        for piece in opponent_pieces:
            if (x, y) in piece.get_legal_moves(piece.position_x, piece.position_y, self):
                return True
        
        return False

    def perform_castling_if_possible(self, king, start_x, start_y, end_y):
        """Check and perform castling move if conditions are met."""
        direction = 1 if end_y > start_y else -1
        rook_pos_y = end_y + direction  # Adjusted rook position
        if self.can_castle(king, start_x, start_y, rook_pos_y):
            self.execute_castling(king, start_x, start_y, rook_pos_y)
            return True
        return False
