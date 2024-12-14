from abc import ABC, abstractmethod

class Piece(ABC):
    def __init__(self, color):
        self.color = color
        self.has_moved = False  # Track if the piece has moved

    @abstractmethod
    def get_legal_moves(self, x, y, board):
        pass

    def move(self, board, start_pos, end_pos):
        if end_pos in self.get_legal_moves(*self.pos_to_index(start_pos), board):
            board.move_piece(start_pos, end_pos)
            self.has_moved = True  # Update has_moved on successful move
            return True
        return False