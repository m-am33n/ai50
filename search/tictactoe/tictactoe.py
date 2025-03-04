"""
Tic Tac Toe Player
"""

import math

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    x_count = 0
    o_count = 0
    for row in board:
        for cell in row:
            if cell == X:
                x_count += 1
            elif cell == O:
                o_count += 1
    if x_count > o_count:
        return O
    return X



def actions(board):
    possible_actions = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                possible_actions.add((i, j))
    return possible_actions



def result(board, action):
    i, j = action
    if i < 0 or i > 2 or j < 0 or j > 2 or board[i][j] != EMPTY:
        raise Exception("Invalid action")
    
    player_turn = player(board)
    board_copy = [row.copy() for row in board]
    board_copy[action[0]][action[1]] = player_turn
    return board_copy


def winner(board):
    for row in board:
        if row[0] == row[1] == row[2] and row[0] != EMPTY:
            return row[0]
        
    for j in range(3):
        if board[0][j] == board[1][j] == board[2][j] and board[0][j] != EMPTY:
            return board[0][j]
    
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != EMPTY:
        return board[0][0]
    
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] != EMPTY:
        return board[0][2]
    return None
    


def terminal(board):
    return actions(board) == set() or winner(board) is not None

def utility(board):
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    return 0

def max_value(board):
    if terminal(board):
        return utility(board), None
    v = -math.inf
    max_value_action = None
    for action in actions(board):
        min_val, _ = min_value(result(board, action))
        if min_val > v:
            v = min_val
            max_value_action = action
        
    return v, max_value_action

def min_value(board):
    if terminal(board):
        return utility(board), None
    v = math.inf
    min_value_action = None
    for action in actions(board):
        max_val, _ = max_value(result(board, action))
        if max_val < v:
            v = max_val
            min_value_action = action
    return v, min_value_action

def minimax(board):
    if terminal(board):
        return None
    
    if player(board) == X:
        max_val, max_action = max_value(board)
        return max_action
    else:
        min_val, min_action = min_value(board)
        return min_action
