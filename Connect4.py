import math
import random as rand
import copy

# -----
# Logic
# -----

def clamp(n, min, max):
    if n < min:
        return min
    elif n > max:
        return max
    else:
        return n

def valid_moves(board):
    return [col for col in range(COLS) if board[col][0] == " "]

def is_illegal(col, game_state):
    # Return "Illegal Move" if the move is illegal
    count = 0
    
    for n in range(0, 7):
        if col != n:
            count += 1
    if count == 7:        
        return True
    
    col = int(col)
    
    if game_state[col][0] != " ":
        return True
    
    return False

def place_piece(board, col, piece):
    new_board = [col.copy() for col in board]

    for row in reversed(range(ROWS)):
        if new_board[col][row] == " ":
            new_board[col][row] = piece
            break

    return new_board

def winning(board, piece):
    # horizontal (by rows)
    for row in range(ROWS):
        for col in range(COLS - (WINC-1)):
            if all(board[col+i][row] == piece for i in range(WINC)):
                return True

    # vertical (by columns)
    for col in range(COLS):
        for row in range(ROWS - (WINC-1)):
            if all(board[col][row+i] == piece for i in range(WINC)):
                return True

    # diagonal down-right
    for col in range(COLS - (WINC-1)):
        for row in range(ROWS - (WINC-1)):
            if all(board[col+i][row+i] == piece for i in range(WINC)):
                return True

    # diagonal up-right
    for col in range(COLS - (WINC-1)):
        for row in range((WINC-1), ROWS):
            if all(board[col+i][row-i] == piece for i in range(WINC)):
                return True
    return False

def game_over(board):
    return (
        winning(board, AI) or
        winning(board, HUMAN) or
        len(valid_moves(board)) == 0
    )
    
# --------
# Evaluate
# --------

# Score window assumes WINC = 4
def score_window(window, piece):
    opp = HUMAN if piece == AI else AI

    if window.count(piece) == 4:
        return 100
    elif window.count(piece) == 3 and window.count(" ") == 1:
        return 5
    elif window.count(piece) == 2 and window.count(" ") == 2:
        return 2
    elif window.count(opp) == 3 and window.count(" ") == 1:
        return -4

    return 0

def evaluate(board):
    score = 0
    # board = [list(row) for row in zip(*copy.deepcopy(board))]

    # center preference
    center = COLS // 2
    center_count = [board[center][row] for row in range(ROWS)].count(AI)
    score += center_count * 3

    # horizontal
    for row in range(ROWS):
        for col in range(COLS - (WINC-1)):
            window = [board[col+i][row] for i in range(WINC)]
            score += score_window(window, AI)

    # vertical
    for col in range(COLS):
        for row in range(ROWS - (WINC-1)):
            window = [board[col][row+i] for i in range(WINC)]
            score += score_window(window, AI)

    # diagonals
    for col in range(COLS - (WINC-1)):
        for row in range(ROWS - (WINC-1)):
            window = [board[col+i][row+i] for i in range(WINC)]
            score += score_window(window, AI)

    for col in range(COLS - (WINC-1)):
        for row in range((WINC-1), ROWS):
            window = [board[col+i][row-i] for i in range(WINC)]
            score += score_window(window, AI)

    return score

# ------------------------
# AI: MINIMAX + ALPHA BETA
# ------------------------

def minimax(board, depth, alpha, beta, maximizing):
    if depth == 0 or game_over(board):
        if winning(board, AI):
            return (None, 100000)
        if winning(board, HUMAN):
            return (None, -100000)
        return (None, evaluate(board))

    moves = valid_moves(board)

    if maximizing:
        value = -math.inf
        best_col = moves[0]

        for col in moves:
            new_board = place_piece(board, col, AI)
            _, new_score = minimax(new_board, depth-1, alpha, beta, False)

            if new_score > value:
                value = new_score
                best_col = col

            alpha = max(alpha, value)
            if alpha >= beta:
                break

        return best_col, value

    else:
        value = math.inf
        best_col = moves[0]

        for col in moves:
            new_board = place_piece(board, col, HUMAN)
            _, new_score = minimax(new_board, depth-1, alpha, beta, True)

            if new_score < value:
                value = new_score
                best_col = col

            beta = min(beta, value)
            if alpha >= beta:
                break

        return best_col, value

def ai_move(board, depth):
    col, _ = minimax(board, depth, -math.inf, math.inf, True)
    return col+1

# -----
# Setup
# -----

ROWS    = 6
COLS    = 7
WINC    = clamp(4, 0, min(ROWS, COLS))
DEPTH   = 5

AI      = "O"
HUMAN   = "X"

init = [
    [" "," "," "," "," "," "],
    [" "," "," "," "," "," "],
    [" "," "," "," "," "," "],
    [" "," "," "," "," "," "],
    [" "," "," "," "," "," "],
    [" "," "," "," "," "," "],
    [" "," "," "," "," "," "]]

# ----
# Game
# ----

def print_game_state(game_state):
    transpose = [list(row) for row in zip(*game_state)]
    
    for row in transpose:
        line = "|"
        
        for item in row:
            line = line + item + "|"
        print(line)

def play_turn(turn, game_state):
    if turn:
        print("What column would you like to put your piece in? ")
        position = input()
        
        while is_illegal(int(position) - 1, game_state):
            print(" ")
            print("That's an illegal move!")
            print("What column would you like to put your piece in? ")
            position = input()
            
        game_state = place_piece(game_state, int(position) - 1, HUMAN)
    else:
        position = ai_move(game_state, DEPTH)
        print(" ")
        print("Your opponent played to column " + str(position))
        
        game_state = place_piece(game_state, int(position) - 1, AI)
        
    print(" ")
    print_game_state(game_state)
    
    return game_state

def main():
    cont = True
    turn = True
    game_state = init
    
    while cont:
        game_state = play_turn(turn, game_state)
        cont = not game_over(game_state)
        
        turn = not turn
    
    print(" ")
    if not turn:
        print("You win!")
    else:
        print("You lose!")    

main()