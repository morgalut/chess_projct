from board.piece import Piece

class Pawn(Piece):
    def __init__(self, color, x, y):
        super().__init__(color)
        self.position_x = x
        self.position_y = y

    def move(self, x, y):
        self.position_x = x
        self.position_y = y

    def get_legal_moves(self, x, y, board, **kwargs):  # Accept additional keyword arguments
        moves = []
        direction = 1 if self.color == 'white' else -1
        start_row = 1 if self.color == 'white' else 6
        # Forward moves
        if board.is_empty(x, y + direction):
            moves.append((x, y + direction))
            if y == start_row and board.is_empty(x, y + 2 * direction):
                moves.append((x, y + 2 * direction))
        # Capture moves
        for dx in [-1, 1]:
            if board.is_opponent_piece(x + dx, y + direction, self.color):
                moves.append((x + dx, y + direction))
        return moves

    def is_valid_move(self, start_x, start_y, end_x, end_y, board):
        legal_moves = self.get_legal_moves(start_x, start_y, board)
        return (end_x, end_y) in legal_moves
