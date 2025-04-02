import random

def generate_sudoku():
    base = 3
    side = base * base
    
    def pattern(r, c):
        return (base * (r % base) + r // base + c) % side
    
    def shuffle(s):
        return random.sample(s, len(s))
    
    r_base = range(base)
    rows = [g * base + r for g in shuffle(r_base) for r in shuffle(r_base)]
    cols = [g * base + c for g in shuffle(r_base) for c in shuffle(r_base)]
    nums = shuffle(range(1, base * base + 1))
    
    board = [[nums[pattern(r, c)] for c in cols] for r in rows]
    
    squares = side * side
    empties = squares * 3 // 4
    for p in random.sample(range(squares), empties):
        board[p // side][p % side] = 0
    
    return board

def is_valid_solution(board, solution):
    base = 3
    side = base * base
    
    def check_rows(board):
        for row in board:
            if len(set(row)) != side:
                return False
        return True
    
    def check_cols(board):
        for col in zip(*board):
            if len(set(col)) != side:
                return False
        return True
    
    def check_squares(board):
        for r in range(0, side, base):
            for c in range(0, side, base):
                square = [board[r + i][c + j] for i in range(base) for j in range(base)]
                if len(set(square)) != side:
                    return False
        return True
    
    return check_rows(solution) and check_cols(solution) and check_squares(solution)
