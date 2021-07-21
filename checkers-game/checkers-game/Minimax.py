import Logic as GL
from Containers import Vector2, PotentialMove
from copy import deepcopy

def is_terminal(gamestate, is_max_player):
    """
    the state of the game, true for over
    :param gamestate:
    :param is_max_player:
    :return: Boolean
    """
    if GL.game_over(gamestate, 2 * is_max_player - 1):
        return True
    return False

def heuristic(gamestate):
    """
    using of heuristic
    :param gamestate:
    :return: val
    """
    val = 0

    for y in range(8):
        for x in range(8):
            val += gamestate[y,x] #breaking abstraction for optimization
    return val

def create_next_gamestate(gamestate, potential_move):
    """
    create the next game state, checker's move
    :param gamestate:
    :param potential_move:
    :return: out
    """
    out = deepcopy(gamestate)
    GL.execute_move(out, potential_move)
    return out

def minimax(gamestate, depth, alpha, beta, is_max_player): # maximizing player is AI (red)
    """
    the algorithm of the Minimax with Alpha-Beta pruning
    :param gamestate:
    :param depth:
    :param alpha:
    :param beta:
    :param is_max_player:
    :return: best_move, value
    """
    if depth == 0 or is_terminal(gamestate, is_max_player):
        return (None, heuristic(gamestate))
    
    best_move = None

    if is_max_player:

        value = float('-inf')
        for potential_move in GL.get_all_potential_moves(gamestate, GL.RED): #get all potential moves for player-->red
            #execute the moving of checkers and create the next game state
            next_gamestate = create_next_gamestate(gamestate, potential_move)
            test_value = minimax(next_gamestate, depth - 1, alpha, beta, False)[1]

            if value < test_value:
                value = test_value
                best_move = potential_move
            
            alpha = max(alpha, value) #alpha

            if alpha >= beta:
                break

        return (best_move, value)
    
    else:

        value = float('inf')
        for potential_move in GL.get_all_potential_moves(gamestate, GL.BLACK): #get all potential moves for player-->black
            # execute the moving of checkers and create the next game state
            next_gamestate = create_next_gamestate(gamestate, potential_move)
            test_value = minimax(next_gamestate, depth - 1, alpha, beta, True)[1]
            
            if value > test_value:
                value = test_value
                best_move = potential_move
            
            beta = min(beta, value) #beta

            if alpha >= beta:
                break

        return (best_move, value)
    