# 7 columns, 6 rows
import random as rand
import copy

init = [
    [" "," "," "," "," "," "],
    [" "," "," "," "," "," "],
    [" "," "," "," "," "," "],
    [" "," "," "," "," "," "],
    [" "," "," "," "," "," "],
    [" "," "," "," "," "," "],
    [" "," "," "," "," "," "]]

def ai(game_state):
    legal_moves = []
    
    for num in range(1,8):
        if not is_illegal(num-1, game_state):
            legal_moves.append(num)
    
    print(legal_moves)
    return legal_moves[rand.randint(0,len(legal_moves)-1)]

def print_game_state(game_state):
    transpose = [list(row) for row in zip(*game_state)]
    
    for row in transpose:
        print(row)

def is_four_vert(game_state):
    for row in range(len(game_state)):
        start = 0
        end = 0
        
        while end < 7:
            li = game_state[row][start:end+1]
            
            if len(set(li)) == 1 and len(li) > 3 and li[0] != " ":
                return True
            elif len(set(li)) == 1:
                end += 1
            elif start < end:
                start += 1
            else:
                start += 1
                end += 1
    
    return False

def is_four_hori(game_state):
    gs = copy.deepcopy(game_state)
    transpose = [list(row) for row in zip(*gs)]
    return is_four_vert(transpose)

def is_four_diag(game_state): 
    # Find the middle 5 diagonals and apply hori
    diagonals = []
    
    for i in range(0, 7-4):
        diagonal1 = []
        diagonal2 = []
        j = 0
        while i + j < 7 and j < 6:
            diagonal1.append(game_state[i+j][j])
            j += 1
        j = 0
        while i + j < 6:
            diagonal2.append(game_state[j][i+j])
            j += 1
        diagonals.append(diagonal1)
        diagonals.append(diagonal2)
    
    for i in range(0, 7-4):
        diagonal1 = []
        diagonal2 = []
        j = 0
        while i + j < 7 and j < 6:
            diagonal1.append(game_state[6 - (i+j)][j])
            j += 1
        j = 0
        while i + j < 6:
            diagonal2.append(game_state[6 - j][i+j])
            j += 1
        diagonals.append(diagonal1)
        diagonals.append(diagonal2)
    return is_four_vert(diagonals)

def check_no_four(game_state):
    # Return True if no four in a row
    # Else return the winning player
    print(is_four_hori(game_state), is_four_vert(game_state), is_four_diag(game_state))
    return not ((is_four_hori(game_state)) or (is_four_vert(game_state)) or (is_four_diag(game_state)))

def piece(turn=True):
    if turn:
        return "X"
    else:
        return "O"
    
def add_piece(col, game_state, turn=True):
    # Return "Illegal Move" if the move is illegal
    count = 0
    
    for n in range(0, 7):
        if col != n:
            count += 1
    if count == 7:        
        return "Illegal Move"
    
    col = int(col)
    
    if game_state[col][0] != " ":
        return "Illegal Move"
    
    for pos in range(len(game_state[col])):
        if pos == 5 or (game_state[col][pos] == " " and game_state[col][pos + 1] != " "):
            game_state[col][pos] = piece(turn)
            break
    
    return game_state

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
    
def play_turn(turn, game_state):
    if turn:
        print("What column would you like to put your piece in? ")
        position = input()
        
        while is_illegal(int(position) - 1, game_state):
            print(" ")
            print("That's an illegal move!")
            print("What column would you like to put your piece in? ")
            position = input()
    else:
        position = ai(game_state)
        print(" ")
        print("Your opponent played to column " + str(position))
    
    game_state = add_piece(int(position) - 1, game_state, turn)
    print(" ")
    print_game_state(game_state)
    
    return game_state

def main():
    cont = True
    turn = True
    game_state = init
    
    while cont:
        game_state = play_turn(turn, game_state)
        cont = check_no_four(game_state)
        
        turn = not turn
        
    if not turn:
        print("You win")
    else:
        print("You lose!")    

main()