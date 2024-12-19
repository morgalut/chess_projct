"""
This module defines the abstract base class for all chess pieces, specifying the template
for defining legal moves and handling move execution.
"""

from abc import ABC, abstractmethod

class Piece(ABC):
    """
    An abstract base class representing a generic chess piece. This class provides
    the structure for defining legal moves and managing piece state.
    """
    
    def __init__(self, color):
        """
        Initializes a new Piece with a specified color.

        Args:
            color (str): The color of the chess piece, typically 'white' or 'black'.
        """
        self.color = color
        self.has_moved = False

    @abstractmethod
    def get_legal_moves(self, x, y, board, **kwargs):
        """
        Determine the legal moves for this piece from position (x, y) on the given board.

        Args:
            x (int): The x-coordinate (column) of the piece's position.
            y (int): The y-coordinate (row) of the piece's position.
            board: The board on which the piece resides.
            **kwargs: Additional keyword arguments that may be required for specific moves.

        Returns:
            list: A list of possible moves as coordinate tuples.
        """
        return []

    def move(self, board, start_pos, end_pos):
        """
        Attempt to move the piece from start_pos to end_pos on the board, if it's a legal move.

        Args:
            board: The board on which the piece resides.
            start_pos (tuple): The starting position (x, y) of the piece.
            end_pos (tuple): The intended end position (x, y) of the piece.

        Returns:
            bool: True if the move was successful, False otherwise.
        """
        if end_pos in self.get_legal_moves(*self.pos_to_index(start_pos), board):
            board.move_piece(start_pos, end_pos)
            self.has_moved = True  # Update has_moved on successful move
            return True
        return False

    def pos_to_index(self, pos):
        """
        Convert a board position in algebraic notation to index notation.

        Args:
            pos (str): The position in algebraic notation, e.g., 'a1'.

        Returns:
            tuple: The position as a tuple of integers (x, y).
        """
        column, row = pos[0], pos[1]
        x = ord(column) - ord('a')
        y = int(row) - 1
        return x, y
