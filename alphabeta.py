from helper import ROWS, COLS
from random import choice as pick_random

def alpha_beta(game, depth, alpha, beta, maximizing_player, current_player):
    '''the alpha beta pruning algorithm, which returns the best move for the current player and its evaluation'''
    if depth == 0: # already checked for win earlier
        eval = evaluate_board(game, current_player)
        return eval, game.board.game_state.copy()

    children = successors(game, current_player)
    best_game_state = pick_random(children)

    if maximizing_player:
        max_eval = float('-inf')
        for child in children:
            winning = child[3]
            if not winning:
                s1, s2, s3 = game.set_gamestate(child[0], child[1], child[2])
                eval, _ = alpha_beta(game, depth - 1, alpha, beta, False, 5 - current_player)
                game.set_gamestate(s1, s2, s3)
            else:
                eval = float('inf')

            if eval > max_eval:
                max_eval = eval
                best_game_state = child

            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval, best_game_state
    else:
        min_eval = float('inf')
        for child in children:
            winning = child[3]
            if not winning:
                s1, s2, s3 = game.set_gamestate(child[0], child[1], child[2])
                eval, _ = alpha_beta(game, depth - 1, alpha, beta, True, 5 - current_player)
                game.set_gamestate(s1, s2, s3)
            else:
                eval = float('-inf')

            if eval < min_eval:
                min_eval = eval
                best_game_state = child

            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval, best_game_state

def successors(game, current_player):
    """Generates all possible successor states for the given game."""
    current_board = game.board.game_state
    successor_states = []

    if game.check_points:
        points = [element for sublist in game.check_points for element in sublist]
        for row_del, col_del in points:
            new_board = current_board.copy()
            new_board[row_del][col_del] = 1
            successor_states.append((new_board, (row_del, col_del), [], False))
    else:
        for row in range(len(current_board)):
            for col in range(len(current_board[row])):
                if game.temp_lock and game.temp_lock[0] == row and game.temp_lock[1] == col:
                    continue
                # Check if the cell is 1
                if current_board[row][col] == 1:
                    # Make a deep copy of the current board state
                    new_board = [row_list.copy() for row_list in current_board]
                    # Replace the 1 with the current player's symbol
                    new_board[row][col] = current_player

                    # check for win
                    lines = game.check_line_gamestate(row, col, new_board, current_player)
                    win = max(lines) >= 5

                    # Add the new board state to the list of successors
                    sandwich = game.sandwich_points_new(new_board, row, col, current_player)
                    if sandwich:
                        sandwiched_points = [chicken_fajita for subway in sandwich for chicken_fajita in subway]
                        for d_row, d_col in sandwiched_points:
                            new_new_board = [row.copy() for row in new_board]
                            new_new_board[d_row][d_col] = 1
                            successor_states.append((new_new_board, (d_row, d_col), [], win))
                    else:
                        successor_states.append((new_board, [], [], win))

    return successor_states

directions = [(1, 0), (0, 1), (1, 1), (-1, -1), (0, -1), (-1, 0)]
line_scores = {1: 5, 2: 10, 3: 50, 4: 100, 5: float('inf')}
free_scores = {1: 0, 2: 1, 3: 2, 4: 8, 5: 9}

def evaluate_board(game, current_player):
    """
    evaluating the board state based on the number of lines made and the number of free ends
    """
    global directions
    global line_scores
    # (-1, 1) and (1, -1) are the directions that do not exist on a hexagonal board, and are thus excluded
    opponent = 5 - current_player
    maximizing = True if current_player == 2 else False
    game_state = game.board.game_state
    game.board.cells = game_state
    score = 0

    for row in range(ROWS):
        for col in range(COLS):
            symbol = game_state[row][col]
            if symbol in (2, 3):
                lines_made = game.check_line_gamestate(row, col, game_state, symbol)
                lines_free = game.check_line_free_gamestate(row, col, game_state, symbol)
                for i in range(3):
                    score += -(5 - 2*symbol) * line_scores[min(5, lines_made[i])]
                    score += -(5 - 2*symbol) * free_scores[min(5, lines_free[i])]

    # Sandwich opportunities
    sandwich_points_player = 0
    sandwich_points_opponent = 0
    for row in range(ROWS):
        for col in range(COLS):
            sandwich_points_player += len(game.sandwich_points_new(game.board.game_state, row, col, 2))
            sandwich_points_opponent -= len(game.sandwich_points_new(game.board.game_state, row, col, 3))
    score += 50 * sandwich_points_player
    score -= 50 * sandwich_points_opponent


    return score
