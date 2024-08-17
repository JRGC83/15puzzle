import random
from functools import reduce

# The solved state of the puzzle for reference
SOLVED_BOARD = (
    (1, 2, 3, 4),
    (5, 6, 7, 8),
    (9, 10, 11, 12),
    (13, 14, 15, 0)  # 0 represents the empty space
)

# Function to shuffle the board
def shuffle_board():
    numbers = list(range(1, 16)) + [0]
    random.shuffle(numbers)
    return tuple(tuple(numbers[i:i + 4]) for i in range(0, 16, 4))

# Function to display the board
def display_board(board):
    return '\n'.join(' '.join(f"{num:2}" for num in row) for row in board)

# Function to find the empty space (0)
def find_empty_space(board):
    return next((i, j) for i, row in enumerate(board) for j, num in enumerate(row) if num == 0)

# Function to move the tile and return a new board
def move_tile(board, direction):
    x, y = find_empty_space(board)
    
    def swap(board, pos1, pos2):
        temp = [list(row) for row in board]  # Convert to mutable lists
        temp[pos1[0]][pos1[1]], temp[pos2[0]][pos2[1]] = temp[pos2[0]][pos2[1]], temp[pos1[0]][pos1[1]]
        return tuple(tuple(row) for row in temp)  # Convert back to immutable tuples
    
    if direction == 'up' and x < 3:
        return swap(board, (x, y), (x + 1, y))
    elif direction == 'down' and x > 0:
        return swap(board, (x, y), (x - 1, y))
    elif direction == 'left' and y < 3:
        return swap(board, (x, y), (x, y + 1))
    elif direction == 'right' and y > 0:
        return swap(board, (x, y), (x, y - 1))
    
    return board

# Function to check if the puzzle is solved
def is_solved(board):
    return board == SOLVED_BOARD

# Function to process a single move and return the updated state
def process_move(board, move):
    return move_tile(board, move)

# Recursive function for the game loop
def play_game(board):
    if is_solved(board):
        return "Congratulations! You've solved the puzzle!"
    
    print(display_board(board))
    move = input("Move (up, down, left, right): ").lower()
    new_board = process_move(board, move)
    
    return play_game(new_board)

# Run the game
if __name__ == "__main__":
    initial_board = shuffle_board()
    print(play_game(initial_board))
