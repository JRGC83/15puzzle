# 15-puzzle game with heuristic and memoization in a single file

# Board manipulation functions

def find_position(board, number):
    return next((i, j) for i, row in enumerate(board) for j, num in enumerate(row) if num == number)

def find_empty_space(board):
    return find_position(board, 0)

def swap_positions(board, pos1, pos2):
    temp_board = [list(row) for row in board]  # Convert to mutable lists
    temp_board[pos1[0]][pos1[1]], temp_board[pos2[0]][pos2[1]] = temp_board[pos2[0]][pos2[1]], temp_board[pos1[0]][pos1[1]]
    return tuple(tuple(row) for row in temp_board)  # Convert back to immutable tuples

def move_tile(board, direction):
    x, y = find_empty_space(board)
    
    move_map = {
        'up': (x + 1, y) if x < 3 else None,
        'down': (x - 1, y) if x > 0 else None,
        'left': (x, y + 1) if y < 3 else None,
        'right': (x, y - 1) if y > 0 else None
    }
    
    new_pos = move_map.get(direction)
    return swap_positions(board, (x, y), new_pos) if new_pos else board

def display_board(board):
    return '\n'.join(' '.join(f"{num:2}" for num in row) for row in board)

SOLVED_BOARD = (
    (1, 2, 3, 4),
    (5, 6, 7, 8),
    (9, 10, 11, 12),
    (13, 14, 15, 0)  # 0 represents the empty space
)

# Heuristic functions

def manhattan_distance(p1, p2):
    """
    Calculate the Manhattan distance between two points p1 and p2.
    """
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

def calculate_manhattan_distance(board):
    """
    Calculate the total Manhattan distance of the board from the solved state.
    """
    total_distance = 0
    for num in range(1, 16):  # Calculate for numbers 1 through 15 only
        current_pos = find_position(board, num)
        correct_pos = find_position(SOLVED_BOARD, num)
        total_distance += manhattan_distance(current_pos, correct_pos)
    return total_distance

def board_to_tuple(board):
    """
    Convert the board into a tuple of tuples to store in a set.
    """
    return tuple(tuple(row) for row in board)

def get_all_moves_distances(board, move_tile_func, last_move=None, seen_boards=None):
    """
    Get the Manhattan distances for all possible immediate moves,
    while avoiding reversing the last move and revisiting previous states.
    """
    if seen_boards is None:
        seen_boards = set()
    
    directions = ['up', 'down', 'left', 'right']
    
    def reverse_direction(direction):
        reverse_map = {
            'up': 'down',
            'down': 'up',
            'left': 'right',
            'right': 'left'
        }
        return reverse_map.get(direction)
    
    moves_distances = {}
    for direction in directions:
        if direction == reverse_direction(last_move):
            continue  # Avoid reversing the last move
        
        next_board = move_tile_func(board, direction)
        next_board_tuple = board_to_tuple(next_board)
        
        if next_board == board or next_board_tuple in seen_boards:
            continue  # Skip invalid moves or previously seen states
        
        seen_boards.add(next_board_tuple)  # Memoize the new board state
        distance = calculate_manhattan_distance(next_board)
        moves_distances[direction] = distance
    
    return moves_distances

# Game loop

def play_game(board):
    seen_boards = set()  # Memoization set to store seen board states

    def game_loop(board, last_move=None):
        print("Current board:")
        print(display_board(board))
        
        if board == SOLVED_BOARD:
            print("Congratulations! You've solved the puzzle!")
            return
        
        # Get the Manhattan distances for all moves, avoiding reverse moves and revisiting states
        moves_distances = get_all_moves_distances(board, move_tile, last_move, seen_boards)
        for move, distance in moves_distances.items():
            print(f"Move {move}: Manhattan Distance = {distance}")
        
        if not moves_distances:
            print("No valid moves available!")
            return

        # Suggest the best move
        best_move = min(moves_distances, key=moves_distances.get)
        print(f"\nSuggested Move: {best_move}")
        
        # Allow the user to enter their move, defaulting to the suggested move
        move = input(f"Enter your move (up, down, left, right) [{best_move}]: ").lower()
        
        if not move:
            move = best_move  # If the user presses Enter, use the suggested move
        
        if move not in ['up', 'down', 'left', 'right'] or move not in moves_distances:
            print("Invalid move. Please choose 'up', 'down', 'left', or 'right'.")
            return game_loop(board, last_move)
        
        # Execute the move and recurse with updated move history
        new_board = move_tile(board, move)
        return game_loop(new_board, last_move=move)
    
    return game_loop(board)

# Main entry point

if __name__ == "__main__":
    # Define a specific initial board state
    initial_board = (
        (5, 1, 2, 3),
        (6, 7, 8, 4),
        (9, 10, 11, 12),
        (13, 14, 0, 15)  # 0 represents the empty space
    )
    
    play_game(initial_board)
