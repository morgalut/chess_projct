# king.py
from board.piece import Piece

class King(Piece):
    def __init__(self, color, x, y):  # Add x, y parameters
        super().__init__(color)
        self.position_x = x  # Store the x position
        self.position_y = y  # Store the y position

    def get_legal_moves(self, x, y, board):
        moves = []
        move_offsets = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        for dx, dy in move_offsets:
            nx, ny = x + dx, y + dy
            if board.is_within_bounds(nx, ny) and (board.get_piece(nx, ny) is None or board.get_piece(nx, ny).color != self.color):
                moves.append((nx, ny))
        return moves