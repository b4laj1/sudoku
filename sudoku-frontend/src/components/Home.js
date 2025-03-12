import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

function Home() {
  const [orgId, setOrgId] = useState('');
  const navigate = useNavigate();

  const handleSubmit = (e) => {
    e.preventDefault();
    if (orgId.trim()) {
      navigate(`/puzzle/${orgId}`);
    }
  };

  return (
    <div className="container">
      <h1>Sudoku Challenge</h1>
      <form onSubmit={handleSubmit}>
        <div>
          <label htmlFor="orgId">Enter Organization ID:</label>
          <input
            type="text"
            id="orgId"
            value={orgId}
            onChange={(e) => setOrgId(e.target.value)}
            required
          />
        </div>
        <button type="submit">Start Challenge</button>
      </form>
    </div>
  );
}

export default Home;