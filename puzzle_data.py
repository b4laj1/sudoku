SUDOKU_PUZZLES = [
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

SUDOKU_SOLUTIONS = [
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

ANAGRAM_PUZZLES = [
    {
        'scrambled': 'mthgliora',
        'hint': 'A step-by-step procedure for solving a problem',
        'solution': 'algorithm'
    },
    {
        'scrambled': 'atabseda',
        'hint': 'A structured collection of data',
        'solution': 'database'
    }
]

MATH_MCQ_PUZZLES = [
    {
        'question': 'What is the time complexity of binary search?',
        'options': ['O(n)', 'O(log n)', 'O(n log n)', 'O(1)'],
        'solution': 1
    },
    {
        'question': 'How many bits are needed to represent numbers from 0 to 1000?',
        'options': ['8 bits', '10 bits', '16 bits', '32 bits'],
        'solution': 2
    }
]

DEV_TRIVIA_PUZZLES = [
    {
        'question': 'Which design pattern is used when you need to ensure a class has only one instance?',
        'options': ['Factory', 'Singleton', 'Observer', 'Strategy'],
        'solution': 1
    },
    {
        'question': 'What does SOLID stand for in software development?',
        'options': [
            'Single Responsibility, Open-Closed, Liskov Substitution, Interface Segregation, Dependency Inversion',
            'Software Object Lifecycle Implementation Design',
            'Structured Object Logic Interface Development',
            'System Organization and Logic Interface Design'
        ],
        'solution': 0
    }
]

# Dictionary mapping puzzle types to their respective puzzles
PUZZLE_TYPES = {
    'SUDOKU': {
        'puzzles': SUDOKU_PUZZLES,
        'solutions': SUDOKU_SOLUTIONS
    },
    'ANAGRAM': {
        'puzzles': ANAGRAM_PUZZLES
    },
    'MATH_MCQ': {
        'puzzles': MATH_MCQ_PUZZLES
    },
    'DEV_TRIVIA': {
        'puzzles': DEV_TRIVIA_PUZZLES
    }
} 