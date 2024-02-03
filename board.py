from helper import generate_board, display_message, ROWS, COLS, CELL_SIZE, screen, WHITE, BLACK, DARK, LIGHT
import pygame

letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
numbers = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']

class Board:
    def __init__(self):
        self.cells = generate_board()
        self.game_state = generate_board()
        pygame.font.init()
        self.font = pygame.font.SysFont('Arial', 20)

    def draw(self):
        '''Draw the board'''
        number_counter = 0

        for row in range(ROWS):
            #number = numbers[row]
            letter = letters[row]
            for col in range(COLS):
                #letter = letters[col]
                number = numbers[col]
                x = col * CELL_SIZE
                y = row * CELL_SIZE
                if self.cells[row][col] == 0:
                    pygame.draw.rect(screen, LIGHT, (x, y, CELL_SIZE, CELL_SIZE))
                elif self.cells[row][col] == 1:
                    pygame.draw.rect(screen, DARK, (x, y, CELL_SIZE, CELL_SIZE))
                    letter = chr(ord('A') + row)
                    number = str(col + 1)
                    text = self.font.render(letter + number, True, BLACK)
                    screen.blit(text, (col * CELL_SIZE, row * CELL_SIZE))
                elif self.cells[row][col] == 2:
                    pygame.draw.circle(screen, DARK, (x + CELL_SIZE // 2, y + CELL_SIZE // 2), CELL_SIZE // 3)
                elif self.cells[row][col] == 3:
                    pygame.draw.circle(screen, WHITE, (x + CELL_SIZE // 2, y + CELL_SIZE // 2), CELL_SIZE // 3)
                pygame.draw.rect(screen, WHITE, (x, y, CELL_SIZE-1, CELL_SIZE-1), 1)  # Grid



    def place_piece(self, row, col, player, temp_lock):
        '''Place a piece on the board'''
        if self.cells[row][col] == 1 and (row, col) != temp_lock:
            self.cells[row][col] = player.symbol
            self.game_state[row][col] = player.symbol
            return True
        return False
