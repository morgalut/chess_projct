# bishop.py
from board.piece import Piece

class Bishop(Piece):
    def __init__(self, color, x, y):  # Add x, y parameters
        super().__init__(color)
        self.position_x = x  # Store the x position
        self.position_y = y  # Store the y position

    def get_legal_moves(self, x, y, board):
        moves = []
        directions = [(-1, -1), (1, -1), (-1, 1), (1, 1)]
        for dx, dy in directions:
            nx, ny = x, y
            while True:
                nx, ny = nx + dx, ny + dy
                if not board.is_within_bounds(nx, ny):
                    break
                if board.get_piece(nx, ny) is None:
                    moves.append((nx, ny))
                elif board.get_piece(nx, ny).color != self.color:
                    moves.append((nx, ny))
                    break
                else:
                    break
        return moves