import React from 'react';

function SudokuPuzzle({ puzzle, solution, onSolutionChange }) {
  const handleCellChange = (rowIndex, colIndex, value) => {
    const newValue = value === '' ? 0 : Math.min(9, Math.max(1, parseInt(value) || 0));
    const newSolution = [...solution];
    newSolution[rowIndex][colIndex] = newValue;
    onSolutionChange(newSolution);
  };

  return (
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
              className={puzzle[rowIndex][colIndex] !== 0 ? 'fixed' : ''}
            />
          ))}
        </div>
      ))}
    </div>
  );
}

export default SudokuPuzzle;
