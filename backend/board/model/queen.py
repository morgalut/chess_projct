from board.piece import Piece

class Queen(Piece):
    def __init__(self, color, x, y):  # Add x, y parameters
        super().__init__(color)
        self.position_x = x  # Store the x position
        self.position_y = y  # Store the y position

    def get_legal_moves(self, x, y, board, **kwargs):  # Accept additional keyword arguments
        moves = []

        # Queen can move like a rook or a bishop
        directions = [
            (1, 0), (-1, 0), (0, 1), (0, -1),  # Rook-like moves
            (1, 1), (1, -1), (-1, 1), (-1, -1)  # Bishop-like moves
        ]

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

    def is_valid_move(self, start_x, start_y, end_x, end_y, board):
        return (end_x, end_y) in self.get_legal_moves(start_x, start_y, board)
