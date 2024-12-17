import React, { useEffect, useState } from 'react';
import { DndProvider, useDrag, useDrop } from 'react-dnd';
import { HTML5Backend } from 'react-dnd-html5-backend';
import { Chess } from 'chess.js';

const chess = new Chess();

interface Piece {
  color: 'w' | 'b'; // Chess.js uses 'w' and 'b' to represent white and black
  type: string; // 'p', 'n', 'b', 'r', 'q', 'k'
  position?: string;
}

interface DragItem {
  id: string;
  piece: Piece;
  type: string;
}

const Square = ({ piece, position, handleMove }: { piece: Piece | null, position: string, handleMove: (from: string, to: string) => void }) => {
  const [{ isDragging }, drag] = useDrag({
    type: 'piece',
    item: { id: position, piece } as DragItem,
    collect: monitor => ({
      isDragging: !!monitor.isDragging(),
    }),
    end: (item: DragItem, monitor) => {
      const dropResult = monitor.getDropResult() as { id?: string } | null;
      if (item && dropResult && dropResult.id) {
        handleMove(item.id, dropResult.id);
      }
    }
  }, [piece, position]);

  const [, drop] = useDrop({
    accept: 'piece',
    drop: () => ({ id: position }),
  });

  return (
    <div ref={drop} style={{
      width: '80px',
      height: '80px',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      backgroundColor: ((parseInt(position[1], 10) + position.charCodeAt(0)) % 2) ? '#b58863' : '#f0d9b5',
      opacity: isDragging ? 0.5 : 1,
    }}>
      {piece && <div ref={drag} style={{ cursor: 'move' }}>
        {piece.type.toUpperCase() + (piece.color === 'w' ? '♕' : '♛')}
      </div>}
    </div>
  );
};

const ChessBoardComponent: React.FC = () => {
  const [board, setBoard] = useState<any[]>(chess.board());

  useEffect(() => {
    setBoard(chess.board());
  }, []);

  const handleMove = (from: string, to: string) => {
    const move = { from, to, promotion: 'q' } as const; // Always promote to a queen for simplicity
    if (chess.move(move)) {
      setBoard(chess.board());
    } else {
      console.error("Invalid move");
    }
  };

  const resetGame = () => {
    chess.reset();
    setBoard(chess.board());
  };

  return (
    <DndProvider backend={HTML5Backend}>
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(8, 80px)', gap: '1px' }}>
        {board.map((row, rowIndex) => row.map((piece: { color: any; type: any; }, colIndex: number) => {
          const position = `${String.fromCharCode('a'.charCodeAt(0) + colIndex)}${8 - rowIndex}`;
          const pieceData = piece ? { color: piece.color, type: piece.type, position } : null;
          return <Square key={position} piece={pieceData} position={position} handleMove={handleMove} />;
        }))}
      </div>
      <button onClick={resetGame} style={{ marginTop: '20px' }}>Reset Game</button>
    </DndProvider>
  );
};

export default ChessBoardComponent;
