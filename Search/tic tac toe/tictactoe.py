"""
Tic Tac Toe Player
"""

import math
from copy import deepcopy

X = "X"
O = "O"
EMPTY = None

DIM = 3

def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    # At first, no X's or O's (in which case, return X). Then, alternate X and O
    count_x = 0
    count_y = 0
    for row in range(len(board)):
        for column in range(len(board[0])):
            if board[row][column] == X:
                count_x += 1
            elif board[row][column] == O:
                count_y += 1
    return X if count_x == count_y else O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    # for every row in board
    # for every column in board
    # if that vector is EMPTY, append the vector tuple to a list
    # Represent the board in a single list
    # actionss = []
    # for row in range(len(board)):
    #     for column in range(len(board[0])):
    #         if board[row][column] == EMPTY:
    #             actionss.append((row, column))

    vec = [x for row in board for x in row]
    valid_action = [(i // DIM, i % DIM) for i in range(len(vec)) if vec[i] == EMPTY]
    return set(valid_action)


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    new_board = deepcopy(board)
    i, j = action
    if (i or j) < 0 or (i or j) >= DIM or board[i][j] != EMPTY:
        raise ValueError("Box is already occupied")

    new_board[i][j] = player(new_board)
    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    vec = [x for row in board for x in row]

    # Checking for a winner via rows
    rows = vec[:3], vec[3:6], vec[6:]
    for row in rows:
        if all(element == row[0] for element in row):
            result = row[0]
            if result is None:
                break
            return result

    # Checking for a winner via columns
    columns = vec[0::3], vec[1::3], vec[2::3]
    for column in columns:
        if all(element == column[0] for element in column):
            result = column[0]
            if result is None:
                break
            return result

    # Checking for a winner diagonally
    indexes1 = [0, 4, 8]
    indexes2 = [2, 4, 6]
    diagonals = [[vec[i] for i in indexes1], [vec[i] for i in indexes2]]
    for diagonal in diagonals:
        if all(element == diagonal[0] for element in diagonal):
            result = diagonal[0]
            if result is None:
                break
            return result

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # If someone has won, game is over and return True
    if winner(board) is not None:
        return True
    # Check if the board is full i.e. actions function return empty set
    elif not actions(board):
        return True
    else:
        return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None
    elif player(board) == X:
        # Call max_value func
        value, move = max_value(board)
        return move
    else:
        # Call min_value func
        value, move = min_value(board)
        return move


def max_value(board):
    if terminal(board):
        return utility(board), None

    v = float('-inf')
    move = None
    for action in actions(board):
        # v = max(v, min_value(result(board, action)))
        action_result, act = min_value(result(board, action))
        if action_result > v:
            move = action
            v = action_result
            if v == 1:
                return v, move

    return v, move


    # function MIN-VALUE(state):
        # if Terminal(state):
            # return Utility(state)
        # v = inf
        # for action in Actions(state):
            # v = Min(v, MAX-VALUE(Result(state, action)))
        # return v
def min_value(board):
    if terminal(board):
        return utility(board), None

    v = float('inf')
    move = None
    for action in actions(board):
        action_result, act = max_value(result(board, action))
        if action_result < v:
            move = action
            v = action_result
            if v == -1:
                return v, move

    return v, move
