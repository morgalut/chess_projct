import React, { useState } from 'react';
import './ChessBoard.css';

// Define the type for the piece symbols to improve type checking
type PieceSymbols = {
  [key: string]: string;
};

const initialBoardSetup = [
  ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R'],
  ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
  [null, null, null, null, null, null, null, null],
  [null, null, null, null, null, null, null, null],
  [null, null, null, null, null, null, null, null],
  [null, null, null, null, null, null, null, null],
  ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
  ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
];

const pieceSymbols: PieceSymbols = {
  'P': '♙', 'R': '♖', 'N': '♘', 'B': '♗', 'Q': '♕', 'K': '♔',
  'p': '♟︎', 'r': '♜', 'n': '♞', 'b': '♝', 'q': '♛', 'k': '♚'
};

const ChessBoard = () => {
  const [board] = useState(initialBoardSetup);
  const [selected, setSelected] = useState<{ x: number, y: number } | null>(null);

  const renderPiece = (piece: string | null) => {
    return piece ? pieceSymbols[piece as keyof PieceSymbols] : '';
  };

  const handleCellClick = (x: number, y: number) => {
    if (selected && selected.x === x && selected.y === y) {
      // Deselect if the same cell is clicked again
      setSelected(null);
    } else {
      // Select the new cell
      setSelected({ x, y });
    }
  };

  return (
    <div className="chessboard">
      {board.map((row, y) => (
        <div key={y} className="row">
          {row.map((cell, x) => (
            <div key={x} className="cell" onClick={() => handleCellClick(x, y)}
                 style={{ backgroundColor: selected && selected.x === x && selected.y === y ? 'lightblue' : 'transparent' }}>
              {renderPiece(cell)}
            </div>
          ))}
        </div>
      ))}
    </div>
  );
};

export default ChessBoard;
