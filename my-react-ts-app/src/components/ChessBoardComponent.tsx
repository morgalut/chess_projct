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
    const loadBoard = async () => {
      try {
        const data = await ChessService.getBoard();
        setBoard({ board: data.board });
        setError(null);  // Clear any previous errors
      } catch (error: any) {
        console.error('Error loading the board:', error);
        setError('Failed to load the board.');
      }
    };

    loadBoard();
  }, []);

  // Converts row and column indices to chess notation
  const indexToNotation = (rowIndex: number, cellIndex: number) => {
    const file = String.fromCharCode('a'.charCodeAt(0) + cellIndex);  // 'a' to 'h'
    const rank = 8 - rowIndex;  // 1 to 8
    return `${file}${rank}`;
  };

  const selectPiece = (rowIndex: number, cellIndex: number) => {
    const position = indexToNotation(rowIndex, cellIndex);
    setSelectedPiece(position);
    fetchPossibleMoves(position);
  };

  const fetchPossibleMoves = async (position: string) => {
    try {
      const moves = await ChessService.getPossibleMoves(position);
      setPossibleMoves(moves); // This will be an array of string positions like ['e3', 'e4']
    } catch (error: any) {
      console.error('Error fetching moves:', error);
      setError('Failed to fetch possible moves.');
    }
  };

  const handleMove = async (rowIndex: any, cellIndex: any) => {
    const endPosition = indexToNotation(rowIndex, cellIndex);
    if (selectedPiece) {
      try {
        const result = await ChessService.makeMove(selectedPiece, endPosition);
        if (result.success && result.board) {
          setBoard({ board: result.board });
          setError(null);
          setSelectedPiece(null); // Clear selection after move
          setPossibleMoves([]); // Clear possible moves
        } else {
          alert(result.message);
        }
      } catch (error: any) {
        console.error('Error making move:', error);
        setError('Failed to make the move.');
      }
    }
  };

// Rendering the chess board
const renderBoard = () => {
    if (!board) return <p>No board data available.</p>;
    const boardToRender = board.board.slice().reverse(); // Reverse to make white start from the bottom of the array
    return boardToRender.map((row, rowIndex) => (
      <div key={rowIndex} style={{ display: 'flex' }}>
        {row.map((cell, cellIndex) => {
          const realRowIndex = board.board.length - 1 - rowIndex; // Adjust rowIndex because of the reversal
          const position = indexToNotation(realRowIndex, cellIndex);
          const isPossibleMove = possibleMoves.includes(position);
          const isSelected = selectedPiece === position;
  
          const handleClick = () => {
            if (isSelected || selectedPiece === null) {
              selectPiece(realRowIndex, cellIndex);
            } else if (isPossibleMove && selectedPiece) {
              handleMove(realRowIndex, cellIndex);
            }
          };
  
          return (
            <div key={cellIndex}
              style={{ width: '50px', height: '50px', border: '1px solid black', display: 'flex', alignItems: 'center', justifyContent: 'center',
                      backgroundColor: isPossibleMove ? 'lightgreen' : isSelected ? 'yellow' : 'transparent' }}
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
    </div>
  );
};

export default ChessBoardComponent;
