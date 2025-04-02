import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import './styles/Anagram.css';

function Anagram() {
  const { orgId } = useParams();
  const navigate = useNavigate();
  const [puzzle, setPuzzle] = useState([]);
  const [solution, setSolution] = useState([]);
  const [puzzleId, setPuzzleId] = useState(null);
  const [timer, setTimer] = useState(0);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Fetch puzzle from backend
    fetch(`http://localhost:5000/api/puzzle?orgId=${orgId}`)
      .then(res => res.json())
      .then(data => {
        if (data.puzzle_type === 'anagram') {
          setPuzzle(data.puzzle);
          setPuzzleId(data.id);
          setSolution(data.puzzle.map(() => ''));
          setLoading(false);
        } else {
          navigate(`/puzzle/${orgId}`);
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

  const handleCellChange = (index, value) => {
    const newSolution = [...solution];
    newSolution[index] = value;
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
      <h1>Anagram Challenge</h1>
      <div className="timer">Time: {formatTime(timer)}</div>
      <div className="anagram-grid">
        {puzzle.map((word, index) => (
          <div key={index} className="anagram-item">
            <span className="anagram-word">{word}</span>
            <input
              type="text"
              value={solution[index]}
              onChange={(e) => handleCellChange(index, e.target.value)}
              className="anagram-input"
            />
          </div>
        ))}
      </div>
      <button className="submit-button" onClick={handleSubmit}>Submit Solution</button>
    </div>
  );
}

export default Anagram;