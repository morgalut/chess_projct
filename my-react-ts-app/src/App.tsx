import React from 'react';
import { useNavigate } from 'react-router-dom';
import ChessBoard from './components/ChessBoard/ChessBoard'; // Import the ChessBoard component

function App() {
  const navigate = useNavigate(); // This is the right place for useNavigate

  // Example function to navigate to "/home"
  const goToHome = () => {
    navigate('/home');
  };

  return (
    <div>
      <h1>Welcome to the App</h1>
      <button onClick={goToHome}>Go to Home Page</button>
      <div>
        <h2>Play Chess</h2>
        <ChessBoard />  {/* Include the ChessBoard component */}
      </div>
    </div>
  );
}

export default App;
