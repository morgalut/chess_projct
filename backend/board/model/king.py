# king.py
from board.model.rook import Rook
from board.piece import Piece

class King(Piece):
    def __init__(self, color, x, y):  # Add x, y parameters
        super().__init__(color)
        self.position_x = x  # Store the x position
        self.position_y = y  # Store the y position

    def get_legal_moves(self, x, y, board):
        moves = super().get_legal_moves(x, y, board)
        if not self.has_moved:
            # Check castling conditions
            moves.extend(self.get_castling_moves(x, y, board))
        return moves

    def get_castling_moves(self, x, y, board):
        castling_moves = []
        # Check for castling rights, ensuring the path is clear and not in check
        if not board.is_in_check(self.color) and not self.has_moved:
            # Kingside castling
            if isinstance(board.get_piece(x, y + 3), Rook) and not board.get_piece(x, y + 3).has_moved:
                if all(board.is_empty(x, y + i) for i in range(1, 3)) and not any(board.is_square_under_attack(x, y + i, self.color) for i in range(1, 3)):
                    castling_moves.append((x, y + 2))
            # Queenside castling
            if isinstance(board.get_piece(x, y - 4), Rook) and not board.get_piece(x, y - 4).has_moved:
                if all(board.is_empty(x, y - i) for i in range(1, 4)) and not any(board.is_square_under_attack(x, y - i, self.color) for i in range(1, 3)):
                    castling_moves.append((x, y - 2))
        return castling_moves