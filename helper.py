import pygame


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
# Constants
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

ROWS = len(alt_board_structure)
COLS = len(alt_board_structure[0])
WIDTH = CELL_SIZE*COLS
HEIGHT = CELL_SIZE*ROWS
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.font.init()
font = pygame.font.SysFont(None, 24)




def generate_board():
    '''Generate the board'''
    board = alt_board_structure
    return board

def display_message(screen, msg):
    '''Display a message on the screen'''
    text_surface = font.render(msg, True, (255, 0, 0))  # RGB value of red color
    text_rect = text_surface.get_rect(center=(WIDTH/2, HEIGHT/2))
    screen.blit(text_surface, text_rect)
    pygame.display.update()
    pygame.time.wait(2000)  # Display the message for 2 seconds (2000 milliseconds)

