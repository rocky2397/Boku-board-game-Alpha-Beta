from board import Board
from player import Player
import pygame
from helper import screen, clock, CELL_SIZE, ROWS, COLS, BLACK, display_message
from alphabeta import alpha_beta
import numpy as np

class Game:
    """The class with the logic for the came"""
    def __init__(self):
        self.board = Board()
        self.player1 = Player(1)
        self.player2 = Player(2)
        self.current_player = self.player1
        self.current_player_symbol = self.current_player.symbol
        self.game_state = self.board.game_state
        self.previous_game_state = None
        self.running = True
        self.temp_lock = None
        self.waiting_for_removal = False
        self.maximizing_player = None
        self.check_points = []
        self.ai = False
        self.ai_player_symbol = None


    @property
    def opponent(self):
        '''Return the opponent'''
        return self.player1 if self.current_player == self.player2 else self.player2

    def opponent_symbol(self):
        '''Return the symbol of the opponent'''
        return 3 if self.current_player == self.player2 else 2

    def check_line(self, start_row, start_col, dx, dy):
        '''Check if there are 5 pieces in a row'''
        count = 0
        row, col = start_row, start_col
        while 0 <= row < ROWS and 0 <= col < COLS:
            # If the position is playable (either empty or occupied by a player)
            if self.board.cells[row][col] != 0:
                # If the position is occupied by the current player
                if self.board.cells[row][col] == self.current_player.symbol:
                    count += 1
                    if count >= 5:
                        return True
                else:
                    count = 0
            row += dy
            col += dx

        return False

    def turn_on_ai(self, player_nr):
        '''Turn on the AI'''
        self.ai = True
        if player_nr == 1:
            self.ai_player_symbol = 3
        else:
            self.ai_player_symbol = 2
        self.maximizing_player = True if player_nr == 1 else False

    def set_gamestate(self, new_game_state, locked_pos, check_points):
        '''Set the game state to a new game state'''
        gamestate_old, self.board.game_state = self.board.game_state, new_game_state
        temp_lock_old, self.temp_lock = self.temp_lock, locked_pos
        check_points_old, self.check_points = self.check_points, check_points
        return gamestate_old, temp_lock_old, check_points_old

    def apply_move(self, new_game_state):
        '''Apply a move to the game state'''
        # Save the current game state to revert back later if needed
        self.previous_game_state = self.game_state.copy()
        self.board.game_state = new_game_state
        # Make any other necessary changes, e.g., switch players


    def revert_move(self):
        '''Revert the last move'''
        # Revert to the previous game state
        self.board.game_state = self.previous_game_state
        self.previous_game_state = None
        # Revert any other changes made in apply_move


    def check_win(self):
        # Check every row for horizontal wins
        for row in range(ROWS):
            if self.check_line(row, 0, 1, 0):
                return True

        # Check every column for vertical wins
        for col in range(COLS):
            if self.check_line(0, col, 0, 1):
                return True

        # Check for diagonal (top-left to bottom-right) wins
        for row in range(ROWS - 4):
            for col in range(COLS - 4):
                if self.check_line(row, col, 1, 1):
                    return True

        return False
    
    def check_line_gamestate(self, row, col, gamestate, current_player_symbol):
        """check the lengths of lines in the grid that are formed of the player's symbol"""
        directions = [(1,0), (0,1), (1,1)]
        line_lengths = []

        for direction in directions:
            line_lengths.append(1)
            c_row, c_col = row + direction[0], col + direction[1]
            while c_row < ROWS and c_col < COLS and c_row >= 0 and c_col >= 0 and gamestate[c_row][c_col] == current_player_symbol:
                line_lengths[-1] += 1
                c_row, c_col = c_row + direction[0], c_col + direction[1]
            c_row, c_col = row - direction[0], col - direction[1]
            while c_row < ROWS and c_col < COLS and c_row >= 0 and c_col >= 0 and gamestate[c_row][c_col] == current_player_symbol:
                line_lengths[-1] += 1
                c_row, c_col = c_row - direction[0], c_col - direction[1]
        return line_lengths
    
    def check_line_free_gamestate(self, row, col, gamestate, opponent_player_symbol):
        """check the lengths of lines in the grid that are free of the opponent's symbol"""
        directions = [(1,0), (0,1), (1,1)]
        line_lengths = []

        for direction in directions:
            line_lengths.append(1)
            c_row, c_col = row + direction[0], col + direction[1]
            while c_row < ROWS and c_col < COLS and c_row >= 0 and c_col >= 0 and gamestate[c_row][c_col] != opponent_player_symbol:
                line_lengths[-1] += 1
                c_row, c_col = c_row + direction[0], c_col + direction[1]
            c_row, c_col = row - direction[0], col - direction[1]
            while c_row < ROWS and c_col < COLS and c_row >= 0 and c_col >= 0 and gamestate[c_row][c_col] != opponent_player_symbol:
                line_lengths[-1] += 1
                c_row, c_col = c_row - direction[0], c_col - direction[1]
        return line_lengths

    def switch_player(self):
        '''Switch the current player'''
        self.current_player = self.opponent
        self.current_player_symbol = self.opponent_symbol()

    def sandwich_points_new(self, game_state, row, col, player_symbol):
        '''Check if in distance of 2 there is a piece of the same color'''
        outer_fit = []
        directions = [(1,0), (0,1), (1,1), (-1,-1), (-1,0), (0,-1)]
        # (-3, 3) and (3, -3) are the directions that do not exist on a hexagonal board, and are thus excluded
        inbetweens = []
        sandwich_points = []
        opponent_symbol = 5 - player_symbol
        for direction in directions:
            r_own, c_own = row + direction[0]*3, col + direction[1]*3
            if 0 <= r_own < ROWS and 0 <= c_own < COLS and game_state[r_own][c_own] == player_symbol:
                initial = (row, col)
                adding = (r_own, c_own)
                outer_fit.append([initial, adding])
            if len(outer_fit) == 1:
                for i in range(2):
                    r_opp, c_opp = row + direction[0]*(i+1), col + direction[1]*(i+1)

                    if 0 <= r_opp < ROWS and 0 <= c_opp < COLS and game_state[r_opp][c_opp] == opponent_symbol:
                        adding = (r_opp, c_opp)
                        inbetweens.append(adding)

            if len(inbetweens) == 2:
                sandwich_points.append(inbetweens)
            outer_fit = []
            inbetweens = []
        return sandwich_points


    def remove_piece(self, x, y):
        '''Remove a piece from the board'''
        opponent_symbol = 5 - self.current_player.symbol
        col, row = x // CELL_SIZE, y // CELL_SIZE
        points_ = self.check_points # here we only need the actually sandwiched points
        points = [element for sublist in points_ for element in sublist]

        if self.board.game_state[row][col] == opponent_symbol and (row, col) in points:
            self.board.game_state[row][col] = 1
            self.board.cells[row][col] = 1
            self.temp_lock = (row, col)
            return True


    def handle_event(self, event, check_points):
        '''Handle the mouse click events/non AI player moves'''
        if self.waiting_for_removal:
            x, y = pygame.mouse.get_pos()
            if self.remove_piece(x, y):
                self.switch_player()
                self.check_points = []
                self.waiting_for_removal = False
                col, row = x // CELL_SIZE, y // CELL_SIZE
                self.temp_lock = (row, col)
            return
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            col, row = x // CELL_SIZE, y // CELL_SIZE

            if self.board.place_piece(row, col, self.current_player, self.temp_lock):
                self.temp_lock = None
                self.check_points = self.sandwich_points_new(self.board.game_state, row, col, self.current_player_symbol)

                if len(self.check_points) != 0:
                    display_message(screen, 'Sandwiched! You have to remove one of the pieces')
                    self.waiting_for_removal = True
                    return

                if self.check_win():
                    print(f"Player {self.current_player.number} wins!")
                    self.running = False
                else:
                    self.switch_player()

    def ai_handling(self):
        '''Handle the AI player moves'''
        print('ai handling')
        if self.waiting_for_removal:
            if self.check_points:
                score, best_move_cluster = alpha_beta(self, depth=2, alpha=float('-inf'), beta=float('inf'),
                                              maximizing_player=self.maximizing_player, current_player=self.ai_player_symbol)
                best_move, _, _, _ = best_move_cluster
                self.board.game_state = best_move
                self.board.cells = best_move
                self.waiting_for_removal = False
                self.check_points = []
        else:
            score, best_move_cluster = alpha_beta(self, depth=2, alpha=float('-inf'), beta=float('inf'),
                                          maximizing_player=self.maximizing_player, current_player=self.ai_player_symbol)
            best_move, best_templock, _, _ = best_move_cluster
            self.board.game_state = best_move
            self.board.cells = best_move
            self.temp_lock = best_templock
        if self.check_win():
            print(f"Player {self.current_player.number} wins!")
            self.running = False
        else:
            self.switch_player()
        return

    def run(self):
        '''Run the game'''
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if self.current_player_symbol == self.ai_player_symbol and self.ai==True:
                    self.ai_handling()
                    self.handle_event(event, self.check_points)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_event(event, self.check_points)


            screen.fill(BLACK)
            self.board.draw()
            pygame.display.flip()
            clock.tick(60)

        pygame.quit()

        winning_state = self.board.game_state
        print('WINNING BOARD STATE:\n')
        for row in winning_state:
            print(row)
            