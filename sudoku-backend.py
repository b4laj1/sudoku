# app.py
from flask import Flask, jsonify, request
import psycopg2
from psycopg2.extras import RealDictCursor
import os
import random
from functools import wraps
from flask_cors import CORS



app = Flask(__name__)
CORS(app)

# Database connection
def get_db_connection():
    conn = psycopg2.connect(
        host=os.environ.get('DB_HOST', 'localhost'),
        database=os.environ.get('DB_NAME', 'sudoku'),
        user=os.environ.get('DB_USER', 'postgres'),
        password=os.environ.get('DB_PASSWORD', 'password')
    )
    conn.autocommit = True
    return conn

# Sample Sudoku puzzles (9x9 grid where 0 represents empty cells)
SAMPLE_PUZZLES = [
    [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9]
    ],
    [
        [0, 0, 0, 2, 6, 0, 7, 0, 1],
        [6, 8, 0, 0, 7, 0, 0, 9, 0],
        [1, 9, 0, 0, 0, 4, 5, 0, 0],
        [8, 2, 0, 1, 0, 0, 0, 4, 0],
        [0, 0, 4, 6, 0, 2, 9, 0, 0],
        [0, 5, 0, 0, 0, 3, 0, 2, 8],
        [0, 0, 9, 3, 0, 0, 0, 7, 4],
        [0, 4, 0, 0, 5, 0, 0, 3, 6],
        [7, 0, 3, 0, 1, 8, 0, 0, 0]
    ]
]

# Solutions for the sample puzzles
SAMPLE_SOLUTIONS = [
    [
        [5, 3, 4, 6, 7, 8, 9, 1, 2],
        [6, 7, 2, 1, 9, 5, 3, 4, 8],
        [1, 9, 8, 3, 4, 2, 5, 6, 7],
        [8, 5, 9, 7, 6, 1, 4, 2, 3],
        [4, 2, 6, 8, 5, 3, 7, 9, 1],
        [7, 1, 3, 9, 2, 4, 8, 5, 6],
        [9, 6, 1, 5, 3, 7, 2, 8, 4],
        [2, 8, 7, 4, 1, 9, 6, 3, 5],
        [3, 4, 5, 2, 8, 6, 1, 7, 9]
    ],
    [
        [4, 3, 5, 2, 6, 9, 7, 8, 1],
        [6, 8, 2, 5, 7, 1, 4, 9, 3],
        [1, 9, 7, 8, 3, 4, 5, 6, 2],
        [8, 2, 6, 1, 9, 5, 3, 4, 7],
        [3, 7, 4, 6, 8, 2, 9, 1, 5],
        [9, 5, 1, 7, 4, 3, 6, 2, 8],
        [5, 1, 9, 3, 2, 6, 8, 7, 4],
        [2, 4, 8, 9, 5, 7, 1, 3, 6],
        [7, 6, 3, 4, 1, 8, 2, 5, 9]
    ]
]

# Initialize database
def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Create tables if they don't exist
    cur.execute('''
    CREATE TABLE IF NOT EXISTS organizations (
        id SERIAL PRIMARY KEY,
        org_id TEXT UNIQUE NOT NULL,
        name TEXT NOT NULL
    )
    ''')
    
    cur.execute('''
    CREATE TABLE IF NOT EXISTS puzzles (
        id SERIAL PRIMARY KEY,
        puzzle_data INTEGER[][] NOT NULL,
        solution_data INTEGER[][] NOT NULL
    )
    ''')
    
    cur.execute('''
    CREATE TABLE IF NOT EXISTS submissions (
        id SERIAL PRIMARY KEY,
        puzzle_id INTEGER REFERENCES puzzles(id),
        org_id TEXT REFERENCES organizations(org_id),
        time_seconds INTEGER NOT NULL,
        completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # Add sample puzzles if they don't exist
    cur.execute('SELECT COUNT(*) FROM puzzles')
    count = cur.fetchone()[0]
    
    if count == 0:
        for i in range(len(SAMPLE_PUZZLES)):
            cur.execute(
                'INSERT INTO puzzles (puzzle_data, solution_data) VALUES (%s, %s)',
                (SAMPLE_PUZZLES[i], SAMPLE_SOLUTIONS[i])
            )
    
    cur.close()
    conn.close()

# Initialize database on startup
init_db()

@app.route('/api/puzzle', methods=['GET'])
def get_puzzle():
    org_id = request.args.get('orgId')
    if not org_id:
        return jsonify({'error': 'Organization ID is required'}), 400
    
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    
    # Check if org exists, create if not
    cur.execute('SELECT * FROM organizations WHERE org_id = %s', (org_id,))
    org = cur.fetchone()
    
    if not org:
        # Create new organization
        cur.execute(
            'INSERT INTO organizations (org_id, name) VALUES (%s, %s) RETURNING *',
            (org_id, f'Organization {org_id}')
        )
        org = cur.fetchone()
    
    # Get a random puzzle
    cur.execute('SELECT id, puzzle_data FROM puzzles ORDER BY RANDOM() LIMIT 1')
    puzzle = cur.fetchone()
    
    cur.close()
    conn.close()
    
    return jsonify({
        'id': puzzle['id'],
        'puzzle': puzzle['puzzle_data']
    })

@app.route('/api/submit', methods=['POST'])
def submit_solution():
    data = request.json
    puzzle_id = data.get('puzzleId')
    org_id = data.get('orgId')
    solution = data.get('solution')
    time_seconds = data.get('time')
    
    if not all([puzzle_id, org_id, solution, time_seconds is not None]):
        return jsonify({'error': 'Missing required fields'}), 400
    
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Get the correct solution
    cur.execute('SELECT solution_data FROM puzzles WHERE id = %s', (puzzle_id,))
    correct_solution = cur.fetchone()[0]
    
    # Check if solution is correct
    is_correct = solution == correct_solution
    
    if is_correct:
        # Record the submission
        cur.execute(
            'INSERT INTO submissions (puzzle_id, org_id, time_seconds) VALUES (%s, %s, %s)',
            (puzzle_id, org_id, time_seconds)
        )
    
    cur.close()
    conn.close()
    
    return jsonify({'correct': is_correct})

@app.route('/api/leaderboard/<int:puzzle_id>', methods=['GET'])
def get_leaderboard(puzzle_id):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    
    cur.execute('''
    SELECT o.name as org_name, s.time_seconds as time, s.completed_at
    FROM submissions s
    JOIN organizations o ON s.org_id = o.org_id
    WHERE s.puzzle_id = %s
    ORDER BY s.time_seconds ASC
    LIMIT 10
    ''', (puzzle_id,))
    
    leaderboard = cur.fetchall()
    
    cur.close()
    conn.close()
    
    return jsonify(leaderboard)

# Serve React app
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    return app.send_static_file('index.html')

if __name__ == '__main__':
    app.run(debug=True)