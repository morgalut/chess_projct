from board.piece import Piece


class Knight(Piece):
    def __init__(self, color, x, y):  # Add x, y parameters
        super().__init__(color)
        self.position_x = x  # Store the x position
        self.position_y = y  # Store the y position

    def get_legal_moves(self, x, y, board):
        moves = []
        potential_moves = [
            (x + 2, y + 1), (x + 2, y - 1),
            (x - 2, y + 1), (x - 2, y - 1),
            (x + 1, y + 2), (x + 1, y - 2),
            (x - 1, y + 2), (x - 1, y - 2),
        ]

        for nx, ny in potential_moves:
            if board.is_within_bounds(nx, ny):
                if board.is_empty(nx, ny) or board.is_opponent_piece(nx, ny, self.color):
                    moves.append((nx, ny))

        return moves