import copy

''' Crate a state that denotes the layout of the board, 
    the current player whos turn it is,
    the children of the current state and
    the depth (number of moves taken in the game up to the current state)
'''
class State:
    def __init__(self, board, player, children=[]):
        self.board = board
        self.player = player
        if player == "h":
            self.score = 2
        else:
            self.score = -2
        self.children = children
        self.depth = count_depth(board)

''' prompts the user to decide who should be first to play,
    the user or
    the program (Jarvis)
'''
def determine_first_to_move():
    print("Would you like to go first (f) or second (s)?")
    answer = input()
    while answer != "f" and answer != "s":
        print("I did not understand, please type 'f' or 's'.")
        print("Would you like to go first (f) or second (s)?")
        answer = input()
    
    if answer == "f":
        return "h"
    return "j"

''' Initialises an empty board '''
def initialise_board():
    return [["_", "_", "_"],
            ["_", "_", "_"],
            ["_", "_", "_"]]

''' define the positions on the board that if occupied by the same player indicate a winning state '''
def winning_states():
    return [[[0,0], [0,1], [0,2]],
            [[1,0], [1,1], [1,2]],
            [[2,0], [2,1], [2,2]],
            [[0,0], [1,0], [2,0]],
            [[0,1], [1,1], [2,1]],
            [[0,2], [1,2], [2,2]],
            [[0,0], [1,1], [2,2]],
            [[0,2], [1,1], [2,0]]]

''' returns whether the board is in a winning state and returns the winner '''
def win(board):
    for states in winning_states():
        loc1, loc2, loc3 = states
        x1, y1 = loc1
        x2, y2 = loc2
        x3, y3 = loc3

        if board[x1][y1] == board[x2][y2] == board[x3][y3]:
            if board[x1][y1] == "X":
                return "You"
            elif board[x1][y1] == "O":
                return "Jarvis"
        
    for x in range(3):
        for y in range(3):
            if board[x][y] == "_":
                return False
    return "Nobody"

''' changes the player to act '''
def change_player(player):
    if player == "h":
        return "j"
    return "h"

''' displayers the result of the game to the user '''
def display_outcome(winner, board):
    display_board(board)
    print()
    print(f"{winner} won.")

''' determines if a position on the board is occupied '''
def occupied(board, location):
    x, y = location
    if board[x][y] == "_":
        return False
    return True

''' displays the board in its current condition '''
def display_board(board):
    for row in board:
        print(row)

''' prompts the user to choose a board position and validates this choice '''
def promt_user_for_choice(board):
    print()
    print("Current Board:")
    display_board(board)
    print()
    print("Your move:")
    position = -1
    x = (position - 1) // 3
    y = position - 1 - x * 3
    while position < 1 or position > 9 or occupied(board, [x, y]):
        print("Please enter the position you'd like to place an 'X' as an integer between 1-9 inclusive.")
        try:
            position = int(input())
            x = (position - 1) // 3
            y = position - 1 - x * 3
        except ValueError:
            print("Value given not an integer")
    x = (position - 1) // 3
    y = position - 1 - x * 3
    return [x, y]

''' finds unoccupied board positions '''
def find_empty_locations(board):
    locations = []
    for x in range(3):
        for y in range(3):
            if board[x][y] == "_":
                locations.append([x, y])
    return locations

''' executes the users or programs choice of move '''
def execute_move(board, player, location):
    x, y = location
    if player == "h":
        board[x][y] = "O"
    else:
        board[x][y] = "X"

''' counts the number of moves that have taken place '''
def count_depth(board):
    counter = 0
    for x in range(3):
        for y in range(3):
            if board[x][y] == "_":
                counter += 1
    return counter

''' determines how 'good' a state is for the program and user in order to determine its move'''
def determine_state_scores(state):
    locations = find_empty_locations(state.board)
    player = change_player(state.player)
    for location in locations:
        new_board = copy.deepcopy(state.board)
        execute_move(new_board, player, location)
        new_state = State(new_board, player)
        state.children.append(new_state)

        result = win(new_board)
        if result:
            if result == "You":
                new_state.score = -1
            elif result == "Jarvis":
                new_state.score = 1
            else:
                new_state.score = 0
        else:
            determine_state_scores(new_state)
        
        score = new_state.score
        if player == "h":
            if score > state.score:
                state.score = score
        else:
            if score < state.score:
                state.score = score

''' enacts a move for the user or program '''
def move(player, board):
    if player == "h":
        x, y = promt_user_for_choice(board)
        board[x][y] = "X"
        print()
        print("Current board:")
        display_board(board)
        print()
        return board
    else:
        print("Jarvis is thinking...")
        state = State(board, player)
        state.children = []
        determine_state_scores(state)
        score = -2
        best_child = None
        for child in state.children:
            if child.depth == state.depth - 1:

                if child.score > score:
                    score = child.score
                    best_child = child
        return best_child.board

''' runs the program to play noughts and crosses '''
def play_naughts_and_crosses():

    player = determine_first_to_move()
    board = initialise_board()
    while not win(board):
        if player == "h":
            board = move("h", board)
        else:
            board = move("j", board)
        player = change_player(player)
    winner = win(board)
    display_outcome(winner, board)

play_naughts_and_crosses()
