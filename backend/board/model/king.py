# king.py
from board.model.rook import Rook
from board.piece import Piece

class King(Piece):
    def __init__(self, color, x, y):
        super().__init__(color)
        self.position_x = x
        self.position_y = y

    def get_legal_moves(self, x, y, board, check_castling=True):
        moves = super().get_legal_moves(x, y, board) or []
        if check_castling and not self.has_moved:
            moves.extend(self.get_castling_moves(x, y, board))
        return moves

    def get_castling_moves(self, x, y, board):
        castling_moves = []
        # Check for castling rights, ensuring the path is clear and not in check
        if not board.is_king_in_check(self.color) and not self.has_moved:  # Use the correctly named method
            # Kingside castling
            if isinstance(board.get_piece(x, y + 3), Rook) and not board.get_piece(x, y + 3).has_moved:
                if all(board.is_empty(x, y + i) for i in range(1, 3)) and not any(board.is_square_under_attack(x, y + i, self.color) for i in range(1, 3)):
                    castling_moves.append((x, y + 2))
            # Queenside castling
            if isinstance(board.get_piece(x, y - 4), Rook) and not board.get_piece(x, y - 4).has_moved:
                if all(board.is_empty(x, y - i) for i in range(1, 4)) and not any(board.is_square_under_attack(x, y - i, self.color) for i in range(1, 3)):
                    castling_moves.append((x, y - 2))
        return castling_moves

    def is_valid_move(self, start_x, start_y, end_x, end_y, board):
        legal_moves = self.get_legal_moves(start_x, start_y, board)
        return (end_x, end_y) in legal_moves