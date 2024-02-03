import pygame
from game import Game

# Initialize pygame
pygame.init()

# Constants
EMPTY = 0
VALID = 1
BLACK_PIECE = 2
WHITE_PIECE = 3
WHITE = (255, 255, 255)

BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
LIGHT = (240, 240, 210)
DARK = (120, 160, 80)
CELL_SIZE = 40
pygame.display.set_caption('Boku')
clock = pygame.time.Clock()

alt_board_structure = [
    [1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 1, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [0, 0, 1, 1, 1, 1, 1, 1, 1, 1],
    [0, 0, 0, 1, 1, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 1, 1, 1, 1, 1, 1]
    ]


ROWS = len(alt_board_structure)
COLS = len(alt_board_structure[0])
WIDTH = CELL_SIZE*COLS
HEIGHT = CELL_SIZE*ROWS
screen = pygame.display.set_mode((WIDTH, HEIGHT))
font = pygame.font.SysFont(None, 24)





if __name__ == "__main__":
    game = Game()
    ai_question = input("Do you want to play against the AI? (y/n)\n")
    if ai_question == "y":
        player_nr = int(input("Which player do you want to be? (1 or 2)\n"
                          "1 will start the game, 2 will go second\n"))
        ai_player = 1 if player_nr== 2 else 2
        game.turn_on_ai(player_nr)
    game.run()