
# Chess Application in Flask

This repository contains a Chess game server implemented in Flask, adhering to the SOLID principles to ensure a robust, maintainable, and scalable application. The server manages game logic, player interactions, and state transitions, offering a RESTful API for chess gameplay.

## Features

- **Create and manage chess games**: Users can start new games, join existing ones, and make moves through a REST API.
- **Real-time game updates**: Utilizes Flask-SocketIO for real-time communication between players.
- **SOLID Design**: Each class and module is designed to fulfill the SOLID principles, enhancing the maintainability and scalability of the application.

## SOLID Principles

The application is structured around the SOLID principles:

- **Single Responsibility Principle**: Each class has a single responsibility and encapsulates only relevant functionalities.
- **Open/Closed Principle**: The system is open for extension but closed for modification.
- **Liskov Substitution Principle**: Derived classes can be substituted for their base classes.
- **Interface Segregation Principle**: Interfaces are specific to client requirements.
- **Dependency Inversion Principle**: High-level modules do not depend on low-level modules. Both should depend on abstractions.

## Architecture

### Classes Overview

- **ChessGame**: Manages the state and rules of a chess game.
- **Player**: Represents a participant in a chess game.
- **GameController**: Handles HTTP requests, delegating chess game actions to the appropriate services.
- **ChessService**: Provides core game functionalities and enforces chess rules.
- **MoveValidator**: Encapsulates the logic for validating chess moves.

### API Endpoints

- `POST /game`: Create a new chess game.
- `POST /game/join`: Join an existing game.
- `POST /game/move`: Make a move in a game.

### Example Requests

```bash
# Start a new game
curl -X POST http://localhost:5000/game

# Join a game
curl -X POST http://localhost:5000/game/join -d "game_id=123&player_id=1"

# Make a move
curl -X POST http://localhost:5000/game/move -d "game_id=123&from=a2&to=a3"
```

## Getting Started

### Prerequisites

- Python 3.8+
- Flask
- Flask-SocketIO

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/morgalut/chess_project.git
   cd chess_project
   ```

2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Change directory to the backend:
   ```bash
   cd backend
   ```

4. Run the server:
   ```bash
   python main.py
   ```

## Testing

The application includes unit tests for all major components. Here are commands to perform some basic move checks:

```bash
# Check White move
curl -X POST http://localhost:5000/move -H "Content-Type: application/json" -d "{\"color\": \"white\", \"start_pos\": \"e2\", \"end_pos\": \"e4\"}"

# Check Black move
curl -X POST http://localhost:5000/move -H "Content-Type: application/json" -d "{\"start_pos\": \"e7\", \"end_pos\": \"e5\"}"
```

To run unit tests:

```bash
python -m unittest discover -s tests
```

