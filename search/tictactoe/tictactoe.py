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
    possible_actions = []
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                possible_actions.append((i, j))
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
        if row[0] == row[1] == row[2]:
            return row[0]
        
    for j in range(3):
        if board[0][j] == board[1][j] == board[2][j]:
            return board[0][j]
    return None
    


def terminal(board):
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                return False
    return True

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
        min_val, min_action = min_value(result(board, action))
        if min_val > v:
            v = min_val
            max_value_action = min_action
        
    return v, max_value_action

def min_value(board):
    if terminal(board):
        return utility(board), None
    v = math.inf
    min_value_action = None
    for action in actions(board):
        max_val, max_action = max_value(result(board, action))
        if max_val < v:
            v = max_val
            min_value_action = max_action
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
