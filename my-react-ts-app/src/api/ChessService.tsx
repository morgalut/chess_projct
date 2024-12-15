import axios from 'axios';

const BASE_URL = 'http://127.0.0.1:5000';

export const getBoard = async () => {
  const response = await axios.get(`${BASE_URL}/board`);
  return response.data;
};

export const makeMove = async (start_pos: string, end_pos: string) => {
  const response = await axios.post(`${BASE_URL}/move`, { start_pos, end_pos });
  return response.data;
};

// New function to fetch possible moves for a given piece
export const getPossibleMoves = async (position: string) => {
  const response = await axios.get(`${BASE_URL}/possible-moves/${position}`); // Adapt URL/path as necessary
  return response.data.moves; // Ensure this matches the structure of the response from your API
};
