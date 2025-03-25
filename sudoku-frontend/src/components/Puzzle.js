import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import SudokuPuzzle from './puzzles/SudokuPuzzle';
import AnagramPuzzle from './puzzles/AnagramPuzzle';
import McqPuzzle from './puzzles/McqPuzzle';

function Puzzle() {
  const { orgId } = useParams();
  const navigate = useNavigate();
  const [puzzleData, setPuzzleData] = useState(null);
  const [solution, setSolution] = useState(null);
  const [timer, setTimer] = useState(0);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Fetch puzzle from backend
    fetch(`http://localhost:5000/api/puzzle?orgId=${orgId}`)
      .then(res => res.json())
      .then(data => {
        setPuzzleData(data);
        // Initialize solution based on puzzle type
        if (data.type === 'SUDOKU') {
          setSolution(data.puzzle.grid.map(row => [...row]));
        } else if (data.type === 'ANAGRAM') {
          setSolution('');
        } else if (['MATH_MCQ', 'DEV_TRIVIA'].includes(data.type)) {
          setSolution(null);
        }
        setLoading(false);
      })
      .catch(err => console.error('Error fetching puzzle:', err));
  }, [orgId]);

  // Timer effect
  useEffect(() => {
    if (!loading) {
      const interval = setInterval(() => {
        setTimer(prevTimer => prevTimer + 1);
      }, 1000);
      return () => clearInterval(interval);
    }
  }, [loading]);

  const handleSubmit = () => {
    fetch('http://localhost:5000/api/submit', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        type: puzzleData.type,
        puzzle_index: puzzleData.puzzle_index,
        orgId,
        solution,
        time: timer
      })
    })
      .then(res => res.json())
      .then(data => {
        if (data.correct) {
          navigate(`/leaderboard/${puzzleData.type}/${puzzleData.puzzle_index}`);
        } else {
          alert('Solution is incorrect! Try again.');
        }
      })
      .catch(err => console.error('Error submitting solution:', err));
  };

  const formatTime = (seconds) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  };

  if (loading) return <div>Loading puzzle...</div>;

  const renderPuzzle = () => {
    switch (puzzleData.type) {
      case 'SUDOKU':
        return (
          <SudokuPuzzle
            puzzle={puzzleData.puzzle.grid}
            solution={solution}
            onSolutionChange={setSolution}
          />
        );
      case 'ANAGRAM':
        return (
          <AnagramPuzzle
            scrambledWord={puzzleData.puzzle.scrambled}
            hint={puzzleData.puzzle.hint}
            solution={solution}
            onSolutionChange={setSolution}
          />
        );
      case 'MATH_MCQ':
      case 'DEV_TRIVIA':
        return (
          <McqPuzzle
            question={puzzleData.puzzle.question}
            options={puzzleData.puzzle.options}
            selectedAnswer={solution}
            onAnswerSelect={setSolution}
          />
        );
      default:
        return <div>Unknown puzzle type</div>;
    }
  };

  return (
    <div className="container">
      <h1>{puzzleData.type.replace('_', ' ')} Challenge</h1>
      <div className="timer">Time: {formatTime(timer)}</div>
      {renderPuzzle()}
      <button onClick={handleSubmit} className="submit-button">
        Submit Solution
      </button>
    </div>
  );
}

export default Puzzle;