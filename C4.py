# 7 columns, 6 rows
init = [
    ["","","","","",""],
    ["","","","","",""],
    ["","","","","",""],
    ["","","","","",""],
    ["","","","","",""],
    ["","","","","",""],
    ["","","","","",""]
]

def print_game_state(game_state):
    print(game_state)

def check_four(game_state):
    return False

def piece(player=True):
    if player:
        return "X"
    else:
        return "O"

def add_piece(player=True, col, state):
    for entry in 