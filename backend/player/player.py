class Player:
    def __init__(self, color):
        self.color = color
        self.start_pos = None
        self.end_pos = None

    def set_move(self, start_pos, end_pos):
        """ Set the move received from the GUI. """
        if self.validate_positions(start_pos, end_pos):
            self.start_pos = start_pos
            self.end_pos = end_pos
            return True
        else:
            return False

    def get_move(self):
        """ Return the last valid move set by the GUI. """
        return self.start_pos, self.end_pos

    def validate_positions(self, start, end):
        """ Validate that the input positions are in correct chess notation. """
        if (len(start) == 2 and len(end) == 2 and
            start[0] in 'abcdefgh' and end[0] in 'abcdefgh' and
            start[1] in '12345678' and end[1] in '12345678'):
            return True
        return False
