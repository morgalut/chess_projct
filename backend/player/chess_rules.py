from board.board import Board


# chess_rules.py
class ChessRules:
    def __init__(self, board):
        self.board = board

    def is_stalemate(self, color):
        """Check if the current player's king is not in check but the player has no legal moves."""
        if self.is_in_check(color):
            return False
        all_pieces = self.board.get_all_pieces(color)
        return not any(self.board.can_move_piece(piece.position_x, piece.position_y) for piece in all_pieces)


    def is_checkmate(self, color):
        """Check if the current player's king is in check and has no legal moves."""
        if not self.is_in_check(color):
            return False
        all_pieces = self.board.get_all_pieces(color)
        return not any(self.board.can_move_piece(x, y) for piece in all_pieces for x, y in [(piece.position_x, piece.position_y)])

    def is_draw_by_insufficient_material(self):
        # Check for a draw by insufficient material
        pieces = self.board.get_all_pieces()
        non_king_pieces = [p for p in pieces if type(p).__name__ != 'King']
        return len(non_king_pieces) <= 2 and all(type(p).__name__ in ['Bishop', 'Knight'] for p in non_king_pieces)

    def is_threefold_repetition(self):
        # Check if current position has occurred three times
        position_count = self.board.position_history[self.board.current_position()]
        return position_count >= 3

    def is_fifty_move_rule(self):
        # Check if the last fifty moves involved no pawn moves or captures
        return self.board.no_capture_or_pawn_move_count >= 50

    def is_in_check(self, color):
        return self.board.is_king_in_check(color)



    def can_move_piece(self, piece, x, y):
        """Check if the piece at position (x, y) can make any legal moves."""
        for dx in range(-8, 9):
            for dy in range(-8, 9):
                nx, ny = x + dx, y + dy
                if self.is_within_bounds(nx, ny):
                    if piece.is_valid_move(x, y, nx, ny, self):
                        return True
        return False
