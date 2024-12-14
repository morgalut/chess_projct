from flask import Flask, request, jsonify
from flask_cors import CORS
from player.player import Player
from board.board import Board
from player.chess_rules import ChessRules  # Import the ChessRules class

app = Flask(__name__)
CORS(app)  # Enable CORS on all routes for all origins
player1 = Player('white')
player2 = Player('black')
current_player = player1
game_board = Board()
rules = ChessRules(game_board)  # Initialize ChessRules with the board

@app.route('/move', methods=['POST'])
def move():
    global current_player
    data = request.json
    print("Received data:", data)  # This will print the data received to the console

    if not data:
        return jsonify({'success': False, 'message': 'No JSON payload provided'}), 400

    start_pos = data.get('start_pos')
    end_pos = data.get('end_pos')

    if not (start_pos and end_pos):
        return jsonify({'success': False, 'message': 'Missing start_pos or end_pos'}), 400

    # Validate positions
    try:
        game_board.pos_to_index(start_pos)
        game_board.pos_to_index(end_pos)
    except ValueError as e:
        return jsonify({'success': False, 'message': str(e)}), 400

    if current_player.set_move(start_pos, end_pos) and game_board.is_legal_move(start_pos, end_pos, current_player.color):
        game_board.move_piece(start_pos, end_pos)
        current_player = player2 if current_player == player1 else player1

        # Check for game over conditions
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
    return jsonify({
        'board': game_board.get_board_state()  # Send the current state of the board
    })

if __name__ == '__main__':
    app.run(debug=True)
