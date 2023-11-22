matrix = [[0] * 8 for _ in range(8)]  # initialize the matrix

matrix = [[0] * 8 for _ in range(8)]  # initialize the matrix


def get_input(current_user):
    # Set the current user name based on the current_user index
    user = "A" if current_user == 0 else "B"
    col = int(input(f"Player {current_user}, Enter the column index (0-7): "))
    row = int(input(f"Player {current_user}, Enter the row index (0-7): "))

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
opponentScoreCol = 0
opponentScoreRow = 0
opponentScoreD = 0

def check_winner(matrix, user):
    # Check rows
    for row in matrix:
        consecutive_count = 0
        for cell in row:
            if cell == user:
                consecutive_count += 1
                if consecutive_count >=4:
                    opponentScoreCol = consecutive_count #check in best move
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
                if consecutive_count >=4:
                    opponentScoreRow = consecutive_count #check in best move
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
                    if consecutive_count >=4:
                        opponentScoreD = consecutive_count #check in best move
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


def evaluate_state(board, player):
    if check_winner(board, player) == player:
        return float("inf")  # Player wins, return maximum score

    if check_winner(board, get_opponent(player)) == get_opponent(player):
        return float("-inf")  # Opponent wins, return minimum score

    return 0  # No winner yet, return neutral score


def get_opponent(player):
    return 'A' if player == 'B' else 'B'


def minimax(board, depth, alpha, beta, maximizing_player):
    if depth == 0 or check_winner(board, 'A') or check_winner(board, 'B'):
        return evaluate_state(board, 'B')

    if maximizing_player:
        max_eval = float('-inf')
        for i in range(len(board)):
            for j in range(len(board[i])):
                if board[i][j] == 0:
                    board[i][j] = 'B'
                    eval = minimax(board, 3 , alpha, beta, False)
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
                    eval = minimax(board, 3, alpha, beta, True)
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

#doesnt block / priority to win plays correctly 
def get_best_move(board):
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
            consecutive_count = has_potential_winning_move(i, j, 'B', board)
            board[i][j] = 0

            if consecutive_count >= 4:
                return move

            # opponent_count = has_potential_winning_move(i, j, 'A', board) # solllve here
            if consecutive_count > best_score:
                best_score = consecutive_count
                best_move = move       
    return best_move


# Main game loop
current_user = 0
game_mode = int(input("Choose the game mode: (0) Player vs. Player, (1) Player vs. AI: "))
while True:
    print("Current Board:")
    for row in matrix:
        print(row)
    print()

    user = "A" if current_user == 0 else "B"
    if current_user == 0 or game_mode == 0:
        current_user = get_input(current_user)
    else:
        print(f"Player {current_user} (Computer) is thinking...")
        best_move = get_best_move(matrix)
        if best_move is None:
            print("The game is a draw!")
            break
        matrix[best_move[0]][best_move[1]] = 'B'
        print(f"Computer placed 'B' at row {best_move[0]} and column {best_move[1]}")

    winner = check_winner(matrix, user)
    if winner:
        print(f"Player {current_user} wins!")
        break

    current_user = 1 - current_user  # Switch player turn

def get_input(current_user):
    # Set the current user name based on the current_user index
    user = "A" if current_user == 0 else "B"
    col = int(input(f"Player {current_user}, Enter the column index (0-7): "))
    row = int(input(f"Player {current_user}, Enter the row index (0-7): "))

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
opponentScoreCol = 0
opponentScoreRow = 0
opponentScoreD = 0

def check_winner(matrix, user):
    # Check rows
    for row in matrix:
        consecutive_count = 0
        for cell in row:
            if cell == user:
                consecutive_count += 1
                if consecutive_count >=4:
                    opponentScoreCol = consecutive_count #check in best move
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
                if consecutive_count >=4:
                    opponentScoreRow = consecutive_count #check in best move
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
                    if consecutive_count >=4:
                        opponentScoreD = consecutive_count #check in best move
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


def evaluate_state(board, player):
    if check_winner(board, player) == player:
        return float("inf")  # Player wins, return maximum score

    if check_winner(board, get_opponent(player)) == get_opponent(player):
        return float("-inf")  # Opponent wins, return minimum score

    return 0  # No winner yet, return neutral score


def get_opponent(player):
    return 'A' if player == 'B' else 'B'


def minimax(board, depth, alpha, beta, maximizing_player):
    if depth == 0 or check_winner(board, 'A') or check_winner(board, 'B'):
        return evaluate_state(board, 'B')

    if maximizing_player:
        max_eval = float('-inf')
        for i in range(len(board)):
            for j in range(len(board[i])):
                if board[i][j] == 0:
                    board[i][j] = 'B'
                    eval = minimax(board, 3 , alpha, beta, False)
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
                    eval = minimax(board, 3, alpha, beta, True)
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

#doesnt block / priority to win plays correctly 
def get_best_move(board):
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
            consecutive_count = has_potential_winning_move(i, j, 'B', board)
            board[i][j] = 0

            if consecutive_count >= 4:
                return move

            # opponent_count = has_potential_winning_move(i, j, 'A', board) # solllve here
            if consecutive_count > best_score:
                best_score = consecutive_count
                best_move = move       
    return best_move


# Main game loop
current_user = 0
game_mode = int(input("Choose the game mode: (0) Player vs. Player, (1) Player vs. AI: "))
while True:
    print("Current Board:")
    for row in matrix:
        print(row)
    print()

    user = "A" if current_user == 0 else "B"
    if current_user == 0 or game_mode == 0:
        current_user = get_input(current_user)
    else:
        print(f"Player {current_user} (Computer) is thinking...")
        best_move = get_best_move(matrix)
        if best_move is None:
            print("The game is a draw!")
            break
        matrix[best_move[0]][best_move[1]] = 'B'
        print(f"Computer placed 'B' at row {best_move[0]} and column {best_move[1]}")

    winner = check_winner(matrix, user)
    if winner:
        print(f"Player {current_user} wins!")
        break

    current_user = 1 - current_user  # Switch player turn
