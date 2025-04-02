from flask import Flask, jsonify, request
import sqlite3
from flask_cors import CORS
from apscheduler.schedulers.background import BackgroundScheduler
from sudoku_generator import generate_sudoku, is_valid_solution
from anagram_generator import generate_anagram, is_valid_anagram_solution
import datetime

app = Flask(__name__)
CORS(app)

# Database connection
def get_db_connection():
    conn = sqlite3.connect('sudoku.db')
    conn.row_factory = sqlite3.Row
    return conn

# Initialize database
def init_db():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute('''
    CREATE TABLE IF NOT EXISTS organizations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        org_id TEXT UNIQUE NOT NULL,
        name TEXT NOT NULL
    )
    ''')

    cur.execute('''
    CREATE TABLE IF NOT EXISTS puzzles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        puzzle_data TEXT NOT NULL,
        puzzle_type TEXT NOT NULL DEFAULT 'sudoku',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    cur.execute('''
    CREATE TABLE IF NOT EXISTS submissions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        puzzle_id INTEGER,
        org_id TEXT,
        time_seconds INTEGER NOT NULL,
        completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (puzzle_id) REFERENCES puzzles(id),
        FOREIGN KEY (org_id) REFERENCES organizations(org_id)
    )
    ''')

    # Add puzzle_type column if it doesn't exist
    cur.execute("PRAGMA table_info(puzzles)")
    columns = [column[1] for column in cur.fetchall()]
    if 'puzzle_type' not in columns:
        cur.execute("ALTER TABLE puzzles ADD COLUMN puzzle_type TEXT NOT NULL DEFAULT 'sudoku'")

    conn.commit()
    cur.close()
    conn.close()

# Initialize a counter
puzzle_counter = 0

# Generate new puzzle every 4 minutes
def generate_puzzle():
    global puzzle_counter
    conn = get_db_connection()
    cur = conn.cursor()

    # Alternate between anagram and sudoku based on the counter
    if puzzle_counter % 2 == 0:
        puzzle = generate_anagram()
        puzzle_type = 'anagram'
    else:
        puzzle = generate_sudoku()
        puzzle_type = 'sudoku'
    
    puzzle_counter += 1
    print(f"Generated puzzle type: {puzzle_type}")  # Debug print

    cur.execute('INSERT INTO puzzles (puzzle_data, puzzle_type) VALUES (?, ?)', (str(puzzle), puzzle_type))
    conn.commit()
    cur.close()
    conn.close()

# Initialize database and scheduler
init_db()
scheduler = BackgroundScheduler()
scheduler.add_job(generate_puzzle, 'interval', minutes=1)
scheduler.start()

@app.route('/api/puzzle', methods=['GET'])
def get_puzzle():
    org_id = request.args.get('orgId')
    if not org_id:
        return jsonify({'error': 'Organization ID is required'}), 400

    conn = get_db_connection()
    cur = conn.cursor()

    # Check if org exists, create if not
    cur.execute('SELECT * FROM organizations WHERE org_id = ?', (org_id,))
    org = cur.fetchone()

    if not org:
        # Create new organization
        cur.execute(
            'INSERT INTO organizations (org_id, name) VALUES (?, ?)',
            (org_id, f'Corp ID {org_id}')
        )
        conn.commit()
        org = cur.execute('SELECT * FROM organizations WHERE org_id = ?', (org_id,)).fetchone()

    # Get the latest puzzle
    cur.execute('SELECT id, puzzle_data, puzzle_type FROM puzzles ORDER BY created_at DESC LIMIT 1')
    puzzle = cur.fetchone()

    if puzzle is None:
        # Generate a new puzzle if none exist
        if puzzle_counter % 2 == 0:
            puzzle_data = generate_anagram()
            puzzle_type = 'anagram'
        else:
            puzzle_data = generate_sudoku()
            puzzle_type = 'sudoku'
        cur.execute('INSERT INTO puzzles (puzzle_data, puzzle_type) VALUES (?, ?)', (str(puzzle_data), puzzle_type))
        conn.commit()
        puzzle_id = cur.lastrowid
        puzzle = {'id': puzzle_id, 'puzzle_data': str(puzzle_data), 'puzzle_type': puzzle_type}
    else:
        print(f"Fetched puzzle type: {puzzle['puzzle_type']}")  # Debug print

    cur.close()
    conn.close()

    return jsonify({
        'id': puzzle['id'],
        'puzzle': eval(puzzle['puzzle_data']),
        'puzzle_type': puzzle['puzzle_type']
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
    cur.execute('SELECT puzzle_data, puzzle_type FROM puzzles WHERE id = ?', (puzzle_id,))
    puzzle = cur.fetchone()
    puzzle_data = eval(puzzle['puzzle_data'])
    puzzle_type = puzzle['puzzle_type']

    # Check if solution is correct
    if puzzle_type == 'sudoku':
        is_correct = is_valid_solution(puzzle_data, solution)
    else:
        is_correct = is_valid_anagram_solution(puzzle_data, solution)

    if is_correct:
        # Record the submission
        cur.execute(
            'INSERT INTO submissions (puzzle_id, org_id, time_seconds) VALUES (?, ?, ?)',
            (puzzle_id, org_id, time_seconds)
        )
        conn.commit()

    cur.close()
    conn.close()

    return jsonify({'correct': is_correct})

@app.route('/api/leaderboard/<int:puzzle_id>', methods=['GET'])
def get_leaderboard(puzzle_id):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute('''
    SELECT o.name as org_name, s.time_seconds as time, s.completed_at
    FROM submissions s
    JOIN organizations o ON s.org_id = o.org_id
    WHERE s.puzzle_id = ?
    ORDER BY s.time_seconds ASC
    LIMIT 10
    ''', (puzzle_id,))

    rows = cur.fetchall()

    leaderboard = []
    for row in rows:
        leaderboard.append({
            'org_name': row['org_name'],
            'time': row['time'],
            'completed_at': row['completed_at']
        })

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