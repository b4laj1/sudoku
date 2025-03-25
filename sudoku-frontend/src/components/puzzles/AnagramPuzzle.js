import React from 'react';

function AnagramPuzzle({ scrambledWord, hint, solution, onSolutionChange }) {
  return (
    <div className="anagram-puzzle">
      <div className="scrambled-word">
        <h2>{scrambledWord}</h2>
      </div>
      <div className="hint">
        <p><strong>Hint:</strong> {hint}</p>
      </div>
      <div className="solution-input">
        <input
          type="text"
          value={solution}
          onChange={(e) => onSolutionChange(e.target.value)}
          placeholder="Enter your solution"
          className="anagram-input"
        />
      </div>
    </div>
  );
}

export default AnagramPuzzle;
