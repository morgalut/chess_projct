"""
This module sets up the Flask application and defines routes for a chess game backend.
It handles game state and player actions.
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from player.player import Player
from player.chess_rules import ChessRules
from board.board import Board

app = Flask(__name__)
CORS(app)

player1 = Player('white')
player2 = Player('black')
current_player = player1
game_board = Board()
rules = ChessRules(game_board)

@app.route('/move', methods=['POST'])
def move():
    """Process a move request from a player and update the game state accordingly."""
    global current_player
    data = request.json
    print("Received data:", data)

    if not data:
        return jsonify({'success': False, 'message': 'No JSON payload provided'}), 400

    color = data.get('color')
    start_pos = data.get('start_pos')
    end_pos = data.get('end_pos')

    if not (color and start_pos and end_pos):
        return jsonify({'success': False, 'message': 'Missing parameters'}), 400

    current_player = player1 if color == 'white' else player2
    print(f"Current player color: {current_player.color}, Move: {start_pos} to {end_pos}")

    try:
        game_board.pos_to_index(start_pos)
        game_board.pos_to_index(end_pos)
    except ValueError as e:
        return jsonify({'success': False, 'message': str(e)}), 400

    if current_player.set_move(start_pos, end_pos) and game_board.is_legal_move(start_pos, end_pos, current_player.color):
        game_board.move_piece(start_pos, end_pos)
        current_player = player2 if current_player == player1 else player1
        print(f"Switched to player color: {current_player.color}")

        if rules.is_checkmate(current_player.color):
            return jsonify({'success': True, 'message': 'Checkmate', 'board': game_board.get_board_state()}), 200
        if rules.is_stalemate(current_player.color):
            return jsonify({'success': True, 'message': 'Stalemate', 'board': game_board.get_board_state()}), 200

        return jsonify({
            'success': True,
            'message': 'Move successful',
            'board': game_board.get_board_state()
        }), 200
    else:
        return jsonify({'success': False, 'message': 'Invalid move'}), 400


@app.route('/board', methods=['GET'])
def get_board():
    """Return the current state of the board."""
    return jsonify({'board': game_board.get_board_state()})


@app.route('/reset', methods=['POST'])
def reset_game():
    """Reset the game to its initial state."""
    global player1, player2, current_player, game_board
    player1 = Player('white')
    player2 = Player('black')
    current_player = player1
    game_board = Board()

    return jsonify({
        'success': True,
        'message': 'Game reset successfully',
        'board': game_board.get_board_state()
    }), 200


if __name__ == '__main__':
    app.run(debug=True)
