import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';

function Leaderboard() {
  const { puzzleType, puzzleIndex } = useParams();
  const [leaderboard, setLeaderboard] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch(`http://localhost:5000/api/leaderboard/${puzzleType}/${puzzleIndex}`)
      .then(res => res.json())
      .then(data => {
        setLeaderboard(data);
        setLoading(false);
      })
      .catch(err => console.error('Error fetching leaderboard:', err));
  }, [puzzleType, puzzleIndex]);

  const formatTime = (seconds) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  };

  if (loading) return <div>Loading leaderboard...</div>;

  return (
    <div className="container">
      <h1>{puzzleType.replace('_', ' ')} Challenge Leaderboard</h1>
      <h3>Puzzle #{parseInt(puzzleIndex) + 1}</h3>
      <div className="leaderboard">
        {leaderboard.length > 0 ? (
          <table>
            <thead>
              <tr>
                <th>Rank</th>
                <th>Organization</th>
                <th>Time</th>
                <th>Completed At</th>
              </tr>
            </thead>
            <tbody>
              {leaderboard.map((entry, index) => (
                <tr key={index}>
                  <td>{index + 1}</td>
                  <td>{entry.org_name}</td>
                  <td>{formatTime(entry.time)}</td>
                  <td>{new Date(entry.completed_at).toLocaleString()}</td>
                </tr>
              ))}
            </tbody>
          </table>
        ) : (
          <p>No submissions yet!</p>
        )}
      </div>
      <Link to="/" className="home-link">Back to Home</Link>
    </div>
  );
}

export default Leaderboard;