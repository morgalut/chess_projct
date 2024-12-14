from board.piece import Piece

class Rook(Piece):
    def __init__(self, color, x, y):  # Add x, y parameters
        super().__init__(color)
        self.position_x = x  # Store the x position
        self.position_y = y  # Store the y position

    def get_legal_moves(self, x, y, board):
        moves = []

        # Horizontal and vertical moves
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            while board.is_within_bounds(nx, ny):
                if board.is_empty(nx, ny):
                    moves.append((nx, ny))
                elif board.is_opponent_piece(nx, ny, self.color):
                    moves.append((nx, ny))
                    break
                else:
                    break
                nx, ny = nx + dx, ny + dy

        return moves
