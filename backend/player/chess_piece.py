# C:\Users\Mor\Desktop\Chess\backend\player\chess_piece.py

class ChessPiece:
    def __init__(self, color):
        if color not in ['white', 'black']:
            raise ValueError("Color must be 'white' or 'black'")
        self.color = color
        self.start_pos = None
        self.end_pos = None

    def set_position(self, start_pos, end_pos):
        """ Set the start and end position for a piece move. """
        self.start_pos = start_pos
        self.end_pos = end_pos

    def get_position(self):
        """ Return the current positions set for this piece. """
        return (self.start_pos, self.end_pos)
