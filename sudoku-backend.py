# app.py
from flask import Flask, jsonify, request
import psycopg2
from psycopg2.extras import RealDictCursor
import os
from functools import wraps
from flask_cors import CORS
from datetime import datetime
from puzzle_data import PUZZLE_TYPES

app = Flask(__name__)
CORS(app)

def get_current_puzzle_info():
    # Get the current week number
    current_date = datetime.now()
    week_number = current_date.isocalendar()[1]
    
    # Determine puzzle type (rotates every week)
    puzzle_types = list(PUZZLE_TYPES.keys())
    current_type = puzzle_types[week_number % len(puzzle_types)]
    
    # Determine puzzle index (cycles through available puzzles)
    available_puzzles = PUZZLE_TYPES[current_type]['puzzles']
    puzzle_index = (week_number // len(puzzle_types)) % len(available_puzzles)
    
    return current_type, puzzle_index

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
    CREATE TABLE IF NOT EXISTS submissions (
        id SERIAL PRIMARY KEY,
        puzzle_type TEXT NOT NULL,
        puzzle_index INTEGER NOT NULL,
        org_id TEXT REFERENCES organizations(org_id),
        time_seconds INTEGER NOT NULL,
        completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
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
        cur.execute(
            'INSERT INTO organizations (org_id, name) VALUES (%s, %s) RETURNING *',
            (org_id, f'Organization {org_id}')
        )
        org = cur.fetchone()
    
    cur.close()
    conn.close()

    # Get current puzzle type and index
    current_type, puzzle_index = get_current_puzzle_info()
    puzzle_data = PUZZLE_TYPES[current_type]['puzzles'][puzzle_index]

    # Format puzzle data based on type
    formatted_puzzle = {}
    if current_type == 'SUDOKU':
        formatted_puzzle = {'grid': puzzle_data}
    elif current_type == 'ANAGRAM':
        formatted_puzzle = {
            'scrambled': puzzle_data['scrambled'],
            'hint': puzzle_data['hint']
        }
    else:  # MATH_MCQ and DEV_TRIVIA
        formatted_puzzle = {
            'question': puzzle_data['question'],
            'options': puzzle_data['options']
        }
    
    return jsonify({
        'type': current_type,
        'puzzle_index': puzzle_index,
        'puzzle': formatted_puzzle
    })

@app.route('/api/submit', methods=['POST'])
def submit_solution():
    data = request.json
    puzzle_type = data.get('type')
    puzzle_index = data.get('puzzle_index')
    org_id = data.get('orgId')
    solution = data.get('solution')
    time_seconds = data.get('time')
    
    if not all([puzzle_type, puzzle_index is not None, org_id, solution, time_seconds is not None]):
        return jsonify({'error': 'Missing required fields'}), 400
    
    # Get the correct solution
    puzzle_data = PUZZLE_TYPES[puzzle_type]['puzzles'][puzzle_index]
    
    # Check if solution is correct based on puzzle type
    is_correct = False
    if puzzle_type == 'SUDOKU':
        correct_solution = PUZZLE_TYPES[puzzle_type]['solutions'][puzzle_index]
        is_correct = solution == correct_solution
    elif puzzle_type == 'ANAGRAM':
        is_correct = solution.lower() == puzzle_data['solution'].lower()
    else:  # MATH_MCQ and DEV_TRIVIA
        is_correct = solution == puzzle_data['solution']
    
    if is_correct:
        # Record the submission
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute(
            'INSERT INTO submissions (puzzle_type, puzzle_index, org_id, time_seconds) VALUES (%s, %s, %s, %s)',
            (puzzle_type, puzzle_index, org_id, time_seconds)
        )
        
        cur.close()
        conn.close()
    
    return jsonify({'correct': is_correct})

@app.route('/api/leaderboard/<string:puzzle_type>/<int:puzzle_index>', methods=['GET'])
def get_leaderboard(puzzle_type, puzzle_index):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    
    cur.execute('''
    SELECT o.name as org_name, s.time_seconds as time, s.completed_at
    FROM submissions s
    JOIN organizations o ON s.org_id = o.org_id
    WHERE s.puzzle_type = %s AND s.puzzle_index = %s
    ORDER BY s.time_seconds ASC
    LIMIT 10
    ''', (puzzle_type, puzzle_index))
    
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