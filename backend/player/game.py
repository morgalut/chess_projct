from board.board import Board
from .player import Player

class Game:
    def __init__(self):
        self.board = Board()
        self.players = [Player('white'), Player('black')]
        self.current_player_index = 0
        self.game_over = False

    def switch_player(self):
        self.current_player_index = 1 - self.current_player_index

    def start(self):
        while not self.game_over:
            self.make_move()
            self.game_over = self.is_game_over()
            if self.game_over:
                print("Game over. Resetting the game.")
                self.reset_game()

    def make_move(self):
        player = self.players[self.current_player_index]
        move = player.get_move(self.board)
        if self.board.is_legal_move(move, player.color):
            self.board.move_piece(move)
            self.switch_player()

    def is_game_over(self):
        # Placeholder logic to check for checkmate, stalemate
        # Implement detailed checks using board state to determine the game end conditions
        if self.check_for_checkmate() or self.check_for_stalemate():
            return True
        return False

    def check_for_checkmate(self):
        # Detailed logic to determine checkmate condition
        return False

    def check_for_stalemate(self):
        # Detailed logic to determine stalemate condition
        return False

    def reset_game(self):
        self.board = Board()  # Re-initialize the board
        self.players = [Player('white'), Player('black')]  # Reinitialize players
        self.current_player_index = 0
        self.game_over = False
        print("Game has been reset. New game can start.")
