import random
import math

matrix = [[0] * 8 for _ in range(8)]  # initialize the matrix for player vs player / board is for player against ai

def print_board():
    """Print board"""

    print("\n  1 2 3 4 5 6 7 8")
    cols = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
    for i in range(8):
        print("{} ".format(cols[i]), end='', flush=True)
        for j in range(8):
            if matrix[i][j] == 0:
                text = "-"
            elif matrix[i][j] == 'A':
                text = "A"
            elif matrix[i][j] == 'B':
                text = "B"
            else:
                # error
                pass
            
            print("{} ".format(text), end='', flush=True)
        print("")


def get_row_column_from_coordinate(coordinate):
    """Converts board coordinate to row and column indices"""
    row = coordinate[0].upper()
    col = int(coordinate[1]) - 1
    rows = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
    row = rows.index(row)
    return row, col

def get_coordinate_from_row_column(row, col):
    """Converts row and column indices to board coordinate"""
    rows = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
    coordinate = rows[row] + str(col + 1)
    return coordinate
def get_input(current_user):
    # Set the current user name based on the current_user index
    user = "A" if current_user == 0 else "B"
    coordinate = input(f"Player {current_user}, Enter your move:")
    # incorrect length
    if not len(coordinate) == 2:
        print("Invalid input, must be in the form of 'xN', where 'x' (row) is a letter between A and H and 'N' (column) is a number between 1 and 8")
        return get_input(current_user)  # Retry input if indices are invalid
    r = coordinate[0].lower()
    c = coordinate[1]

			# make sure col is a number
    rows = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    if not r in rows:
        print(" Invalid input, row index must be between A and H")
        return get_input(current_user)  # Retry input if indices are invalid
			
    col_index = int(c)
    if col_index < 1 or col_index > 8:
        print(" Invalid input, column index must be between 1 and 8")
        return get_input(current_user)  # Retry input if indices are invalid
    
    row, col = get_row_column_from_coordinate(coordinate)

    if row < 0 or row > 7 or col < 0 or col > 7:
        print("Invalid indices. Please try again.")
        return get_input(current_user)  # Retry input if indices are invalid

    if matrix[row][col] != 0:
        print("This position already has data. Please choose a different position.")
        return get_input(current_user)  # Retry input if position already has data

    # Check if the chosen position follows the rules
    if col not in [0, 7]:
        if matrix[row][col - 1] == 0 and matrix[row][col + 1] == 0:
            print("Invalid position. Please choose a position on the edges or next to an already placed index.")
            return get_input(current_user)  # Retry input if position doesn't follow the rules

    matrix[row][col] = user
    return current_user


def check_winner(matrix, user):
    # Check rows
    for row in matrix:
        consecutive_count = 0
        for cell in row:
            if cell == user:
                consecutive_count += 1
                if consecutive_count >= 5:
                    return user
            else:
                consecutive_count = 0

    # Check columns
    for col in range(len(matrix[0])):
        consecutive_count = 0
        for row in range(len(matrix)):
            if matrix[row][col] == user:
                consecutive_count += 1
                if consecutive_count >= 5:
                    return user
            else:
                consecutive_count = 0

    # Check diagonals
    for i in range(len(matrix) - 4):
        for j in range(len(matrix[0]) - 4):
            consecutive_count = 0
            for k in range(5):
                if matrix[i + k][j + k] == user:
                    consecutive_count += 1
                    if consecutive_count >= 5:
                        return user
                else:
                    consecutive_count = 0

            consecutive_count = 0
            for k in range(5):
                if matrix[i + k][j + 4 - k] == user:
                    consecutive_count += 1
                    if consecutive_count >= 5:
                        return user
                else:
                    consecutive_count = 0

    return None

def minimax(board, depth, alpha, beta, maximizing_player):
    if depth == 0 or check_winner(board, 'A') or check_winner(board, 'B'):
        return evaluate_state(board, 'B')

    if maximizing_player:
        max_eval = float('-inf')
        for i in range(len(board)):
            for j in range(len(board[i])):
                if board[i][j] == 0:
                    board[i][j] = 'B'
                    eval = minimax(board, depth-1, alpha, beta, False)
                    board[i][j] = 0
                    max_eval = max(max_eval, eval)
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        break  # Beta cutoff
        return max_eval
    else:
        min_eval = float('inf')
        for i in range(len(board)):
            for j in range(len(board[i])):
                if board[i][j] == 0:
                    board[i][j] = 'A'
                    eval = minimax(board, depth-1, alpha, beta, True)
                    board[i][j] = 0
                    min_eval = min(min_eval, eval)
                    beta = min(beta, eval)
                    if beta <= alpha:
                        break  # Alpha cutoff
        return min_eval


def get_possible_moves(board):
    moves = []
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == 0:
                moves.append((i, j))
    return moves


def count_consecutive_pieces(row, col, direction, player, board):
    count = 0
    while row >= 0 and row < len(board) and col >= 0 and col < len(board[row]) and board[row][col] == player:
        count += 1
        row += direction[0]
        col += direction[1]
    return count

def has_potential_winning_move(row, col, player, board):
    directions = [(0, 1), (1, 0), (1, 1), (-1, 1)]  # Right, Down, Diagonal Down-Right, Diagonal Up-Right

    max_consecutive = 0
    for direction in directions:
        count_forward = count_consecutive_pieces(row + direction[0], col + direction[1], direction, player, board)
        count_backward = count_consecutive_pieces(row - direction[0], col - direction[1], (-direction[0], -direction[1]), player, board)

        consecutive_count = count_forward + count_backward
        if consecutive_count >= 4:
            return consecutive_count

        max_consecutive = max(max_consecutive, consecutive_count)

    return max_consecutive

def get_opponent(player):
    return 'A' if player == 'B' else 'B'

#doesnt block / priority to win plays correctly 
def evaluate_state(board, player):
    opponent = get_opponent(player)
    if check_winner(board, player) == player:
        return float("inf")  # Player wins, return maximum score

    if check_winner(board, opponent) == opponent:
        return float("-inf")  # Opponent wins, return minimum score

def evaluate_board(board):
    """Evaluates the board state for the AI player"""
    if check_winner(board, 'B'):
        return 1  # AI wins
    elif check_winner(board, 'A'):
        return -1  # Human wins
    else:
        return 0  # Draw or game in progress

def isValid(board, i, j):
    # Check if the move follows the game rules
            if j not in [0, 7] and (board[i][j - 1] == 0 and board[i][j + 1] == 0):
                return False   # Move doesn't follow the rules, skip it
            return True # Move is valid











# def get_best_move(board):
#     best_score = float('-inf')
#     best_move = None
#     moves = get_possible_moves(board)

#     for move in moves:
#         i, j = move
#         if board[i][j] == 0:
#             # Check if the move follows the game rules
#             if j not in [0, 7] and (board[i][j - 1] == 0 and board[i][j + 1] == 0):
#                 continue  # Move doesn't follow the rules, skip it

#             board[i][j] = 'B'
#             ai_consecutive_count = has_potential_winning_move(i, j, 'B', board)
#             opponent_consecutive_count = has_potential_winning_move(i, j, 'A', board)
#             board[i][j] = 0

#             if opponent_consecutive_count >= 4 and ai_consecutive_count < 4:
#                 # Blocking move, return immediately
#                 return move

#             # Adjust the scoring logic to prioritize blocking only when opponent's count is at least four
#             if opponent_consecutive_count >= 4:
#                 score = opponent_consecutive_count * 2
#             else:
#                 score = ai_consecutive_count

#             if score > best_score:
#                 best_score = score
#                 best_move = move
#     return best_score
#     # return best_move




def minimax(board, depth, alpha, beta, maximizing_player):
    """Minimax algorithm implementation with alpha-beta pruning"""
    if depth == 0 or check_winner(board, 'A') or check_winner(board, 'B'):
        return evaluate_board(board)

    if maximizing_player:
        max_eval = -math.inf
        for move in get_possible_moves(board):
            row, col = move
            board[row][col] = 'B'
            eval = minimax(board, depth - 1, alpha, beta, False)
            board[row][col] = 0
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break  # Beta cutoff
        return max_eval

    else:
        min_eval = math.inf
        for move in get_possible_moves(board):
            row, col = move
            board[row][col] = 'A'
            eval = minimax(board, depth - 1, alpha, beta, True)
            board[row][col] = 0
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break  # Alpha cutoff
        return min_eval



def get_best_move(board,temperature):
    best_score = float('-inf')
    best_move = None
    moves = get_possible_moves(board)

    for move in moves:
        i, j = move
        if board[i][j] == 0:
            # Check if the move follows the game rules
            if j not in [0, 7] and (board[i][j - 1] == 0 and board[i][j + 1] == 0):
                continue  # Move doesn't follow the rules, skip it

            board[i][j] = 'B'
            eval = minimax(board, 2, -math.inf, math.inf, False)  # Depth is set to 5 for example purposes

            ai_consecutive_count = has_potential_winning_move(i, j, 'B', board)
            opponent_consecutive_count = has_potential_winning_move(i, j, 'A', board)
            board[i][j] = 0

            if opponent_consecutive_count >= 4 and ai_consecutive_count < 4:
                return move
                # best_move = move

            # Adjust the scoring logic to prioritize blocking only when opponent's count is at least four
            if opponent_consecutive_count >= 4:
                score = opponent_consecutive_count * 2
            else:
                score = ai_consecutive_count

            if score > best_score:
                best_score = score
                best_move = move
            if eval > best_score:
                best_score = eval
                best_move = move
            elif temperature > 0:
                probability = math.exp((eval - best_eval) / temperature)
                if random.random() < probability:
                    best_eval = eval
                    best_move = move

        
         
    return best_move


# Main game loop
# ...
temperature = 1.0  # Initial temperature

def main():
    # Main game loop
    current_user = 0
    game_mode = int(input("Choose the game mode:\n-1 Player vs. Player\n-2 Player vs. AI\n"))
    if game_mode == 2:
        symbol = input("Choose your player symbol ('A' or 'B'): ").upper()
        if symbol == 'A':
            current_user = 0
            opponent_symbol = 'B'
        else:
            current_user = 1
            opponent_symbol = 'A'
            
    while True:
        print("Current Board:")
        print_board()

        user = "A" if current_user == 0 else "B"
        if current_user == 0 or game_mode == 1:
            current_user = get_input(current_user)
        else:
            print(f"Player {current_user} (Computer) is thinking...")
            # best_move = get_best_move(matrix,2)  # Pass the depth as an argument
            row, col = get_best_move(matrix,0)  # Pass the temperature to get_best_move

            # if best_move is None:      #editttt draaw
            #     print("The game is a draw!")
            #     break
            # matrix[best_move[0]][best_move[1]] = user
            matrix[row][col] = 'B'
            # temperature -= 0.1  # Decrease the temperature

            # if temperature < 0:
            #     temperature = 0

            x = get_coordinate_from_row_column(row,col)
            print(f"Computer placed 'B' at {x}")

        winner = check_winner(matrix, user)
        if winner:
            print("Player {user} Win!")
            print("Final Board:")
            print_board()
            break

        current_user = 1 - current_user  # Switch player turn

main()
