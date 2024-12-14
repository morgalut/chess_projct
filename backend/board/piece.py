from abc import ABC, abstractmethod

class Piece(ABC):
    def __init__(self, color):
        self.color = color

    @abstractmethod
    def get_legal_moves(self, x, y, board):
        """Generate all legal moves for this piece."""
        pass

    def move(self, board, start_pos, end_pos):
        if (end_pos in self.get_legal_moves(*self.pos_to_index(start_pos), board)):
            board.move_piece(start_pos, end_pos)
            return True
        return False

