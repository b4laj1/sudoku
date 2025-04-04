import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import './styles/Puzzle.css';

function Puzzle() {
  const { orgId } = useParams();
  const navigate = useNavigate();
  const [puzzle, setPuzzle] = useState(null);
  const [solution, setSolution] = useState([]);
  const [puzzleId, setPuzzleId] = useState(null);
  const [timer, setTimer] = useState(0);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Fetch puzzle from backend
    fetch(`http://localhost:5000/api/puzzle?orgId=${orgId}`)
      .then(res => res.json())
      .then(data => {
        if (data.puzzle_type === 'sudoku') {
          setPuzzle(data.puzzle);
          setPuzzleId(data.id);
          const initialSolution = data.puzzle.map(row => [...row]);
          setSolution(initialSolution);
          setLoading(false);
        } else {
          navigate(`/anagram/${orgId}`);
        }
      })
      .catch(err => console.error('Error fetching puzzle:', err));
  }, [orgId, navigate]);

  // Timer effect
  useEffect(() => {
    if (!loading) {
      const interval = setInterval(() => {
        setTimer(prevTimer => prevTimer + 1);
      }, 1000);
      return () => clearInterval(interval);
    }
  }, [loading]);

  const handleCellChange = (rowIndex, colIndex, value) => {
    const newValue = value === '' ? 0 : Math.min(9, Math.max(1, parseInt(value) || 0));
    const newSolution = [...solution];
    newSolution[rowIndex][colIndex] = newValue;
    setSolution(newSolution);
  };

  const handleSubmit = () => {
    fetch('http://localhost:5000/api/submit', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        puzzleId,
        orgId,
        solution,
        time: timer
      })
    })
      .then(res => res.json())
      .then(data => {
        if (data.correct) {
          navigate(`/leaderboard/${puzzleId}`);
        } else {
          alert('Solution is incorrect! Try again.');
        }
      })
      .catch(err => console.error('Error submitting solution:', err));
  };

  if (loading) return <div>Loading puzzle...</div>;

  const formatTime = (seconds) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  };

  return (
    <div className="container">
      <h1>Sudoku Challenge</h1>
      <div class="timer-container">
        <div class="timer">Time: {formatTime(timer)}</div>
      </div>
      <div className="puzzle-grid">
        {solution.map((row, rowIndex) => (
          <div key={rowIndex} className="row">
            {row.map((cell, colIndex) => (
              <input
                key={`${rowIndex}-${colIndex}`}
                type="number"
                min="1"
                max="9"
                value={cell || ''}
                onChange={(e) => handleCellChange(rowIndex, colIndex, e.target.value)}
                disabled={puzzle[rowIndex][colIndex] !== 0}
                className={`cell ${puzzle[rowIndex][colIndex] !== 0 ? 'fixed' : ''}`}
              />
            ))}
          </div>
        ))}
      </div>
      <div class="button-container">
        <button onClick={handleSubmit} className="submit-button">
          Submit Solution
        </button>
      </div>
    </div>
  );
}

export default Puzzle;