import React from 'react';

function McqPuzzle({ question, options, selectedAnswer, onAnswerSelect }) {
  return (
    <div className="mcq-puzzle">
      <div className="question">
        <h3>{question}</h3>
      </div>
      <div className="options">
        {options.map((option, index) => (
          <div key={index} className="option">
            <label>
              <input
                type="radio"
                name="mcq-answer"
                value={index}
                checked={selectedAnswer === index}
                onChange={() => onAnswerSelect(index)}
              />
              {option}
            </label>
          </div>
        ))}
      </div>
    </div>
  );
}

export default McqPuzzle;
