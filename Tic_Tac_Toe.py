# Tic-Tac-Toe AI using Minimax Algorithm
# Human is 'X', AI is 'O'

# Initialize the board
board = [' ' for _ in range(9)]  # 0-8 positions

# Function to display the board
def print_board(board):
    print()
    for i in range(3):
        print(board[i*3] + ' | ' + board[i*3+1] + ' | ' + board[i*3+2])
        if i < 2:
            print('--+---+--')
    print()

# Function to check if there is a winner
def check_winner(board):
    # Winning combinations
    win_combinations = [
        [0,1,2], [3,4,5], [6,7,8],  # rows
        [0,3,6], [1,4,7], [2,5,8],  # columns
        [0,4,8], [2,4,6]            # diagonals
    ]
    for combo in win_combinations:
        if board[combo[0]] == board[combo[1]] == board[combo[2]] != ' ':
            return board[combo[0]]  # returns 'X' or 'O'
    return None

# Human player move
def human_move(board):
    move = input("Enter your move (1-9): ")
    if not move.isdigit() or int(move) not in range(1,10):
        print("Invalid input! Enter a number 1-9.")
        human_move(board)
        return
    move = int(move) - 1
    if board[move] == ' ':
        board[move] = 'X'
    else:
        print("Position already taken! Try again.")
        human_move(board)

# AI using Minimax
def minimax(board, depth, is_maximizing):
    winner = check_winner(board)
    if winner == 'O':
        return 1
    elif winner == 'X':
        return -1
    elif ' ' not in board:
        return 0

    if is_maximizing:
        best_score = -float('inf')
        for i in range(9):
            if board[i] == ' ':
                board[i] = 'O'
                score = minimax(board, depth+1, False)
                board[i] = ' '
                best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for i in range(9):
            if board[i] == ' ':
                board[i] = 'X'
                score = minimax(board, depth+1, True)
                board[i] = ' '
                best_score = min(score, best_score)
        return best_score

# AI chooses the best move
def ai_move(board):
    best_score = -float('inf')
    move = None
    for i in range(9):
        if board[i] == ' ':
            board[i] = 'O'
            score = minimax(board, 0, False)
            board[i] = ' '
            if score > best_score:
                best_score = score
                move = i
    board[move] = 'O'

# Game loop
def play_game():
    print("Welcome to Tic-Tac-Toe! You are X, AI is O.")
    print_board(board)

    while True:
        human_move(board)
        print_board(board)
        if check_winner(board) == 'X':
            print("Congratulations! You won!")
            break
        elif ' ' not in board:
            print("It's a draw!")
            break

        print("AI's turn:")
        ai_move(board)
        print_board(board)
        if check_winner(board) == 'O':
            print("AI wins! Better luck next time.")
            break
        elif ' ' not in board:
            print("It's a draw!")
            break

# Start the game
play_game()
