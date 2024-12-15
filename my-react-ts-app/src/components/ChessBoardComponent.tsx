import React, { useEffect, useState } from 'react';
import * as ChessService from '../api/ChessService';

interface Piece {
  color: string;
  type: string;
}

interface BoardProps {
  board: (Piece | null)[][];
}

const ChessBoardComponent = () => {
  const [board, setBoard] = useState<BoardProps | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [selectedPiece, setSelectedPiece] = useState<string | null>(null);
  const [possibleMoves, setPossibleMoves] = useState<string[]>([]);

  useEffect(() => {
    loadBoard();
  }, []);

  const loadBoard = async () => {
    try {
      const data = await ChessService.getBoard();
      setBoard({ board: data.board });
      setError(null);
    } catch (error: any) {
      console.error('Error loading the board:', error);
      setError('Failed to load the board.');
    }
  };

  const handleReset = async () => {
    try {
      const result = await ChessService.resetGame();
      if (result.success) {
        setBoard({ board: result.board });
        setError(null);
      } else {
        setError('Failed to reset the game.');
      }
    } catch (error: any) {
      console.error('Error resetting the game:', error);
      setError('Failed to reset the game.');
    }
  };

  const indexToNotation = (rowIndex: number, cellIndex: number) => {
    const file = String.fromCharCode('a'.charCodeAt(0) + cellIndex);
    const rank = 8 - rowIndex;
    return `${file}${rank}`;
  };

  const selectPiece = (rowIndex: number, cellIndex: number) => {
    const position = indexToNotation(rowIndex, cellIndex);
    if (selectedPiece === position) {
      setSelectedPiece(null);
      setPossibleMoves([]);
    } else {
      setSelectedPiece(position);
      // Here you might need to load possible moves for the selected piece
      // This part of the code can be adjusted as per your backend capabilities to provide possible moves
    }
  };

  const handleMove = async (rowIndex: number, cellIndex: number) => {
    const endPosition = indexToNotation(rowIndex, cellIndex);
    if (selectedPiece && possibleMoves.includes(endPosition)) {
      try {
        const result = await ChessService.makeMove(selectedPiece, endPosition);
        if (result.success && result.board) {
          setBoard({ board: result.board });
          setError(null);
          setSelectedPiece(null);
          setPossibleMoves([]);
        } else {
          setError(result.message);
        }
      } catch (error: any) {
        console.error('Error making move:', error);
        setError('Failed to make the move.');
      }
    }
  };

  const renderBoard = () => {
    if (!board) return <p>No board data available.</p>;
    const boardToRender = board.board.slice().reverse();
    return boardToRender.map((row, rowIndex) => (
      <div key={rowIndex} style={{ display: 'flex' }}>
        {row.map((cell, cellIndex) => {
          const realRowIndex = board.board.length - 1 - rowIndex;
          const position = indexToNotation(realRowIndex, cellIndex);
          const isPossibleMove = possibleMoves.includes(position);
          const isSelected = selectedPiece === position;

          const handleClick = () => {
            if (isPossibleMove && selectedPiece) {
              handleMove(realRowIndex, cellIndex);
            } else {
              selectPiece(realRowIndex, cellIndex);
            }
          };

          return (
            <div key={cellIndex}
              style={{
                width: '50px', height: '50px', border: '1px solid black', display: 'flex',
                alignItems: 'center', justifyContent: 'center',
                backgroundColor: isSelected ? 'yellow' : isPossibleMove ? 'lightgreen' : 'transparent'
              }}
              onClick={handleClick}
            >
              {cell ? `${cell.type} ${cell.color}` : '-'}
            </div>
          );
        })}
      </div>
    ));
  };

  return (
    <div>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      <div>{renderBoard()}</div>
      <button onClick={handleReset} style={{ margin: '10px', padding: '10px' }}>Reset Game</button>
    </div>
  );
};

export default ChessBoardComponent;
