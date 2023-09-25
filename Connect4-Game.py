import numpy as np
import pygame
import sys
import random

# Constants
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
ROW_COUNT = 6
COLUMN_COUNT = 7

# ... (previous code)
def create_board():
    board = np.zeros((ROW_COUNT, COLUMN_COUNT))
    return board

def drop_piece(board, row, col, piece):
    board[row][col] = piece

def is_valid(board, col):
    return board[ROW_COUNT-1][col] == 0

def get_next_open_row(board, col):
    for i in range(ROW_COUNT):
        if board[i][col] == 0:
            return i

def print_board(board):
    print(np.flip(board, 0))

def winning_board(board, piece):
    for x in range(COLUMN_COUNT - 3):
        for y in range(ROW_COUNT):
            if board[y][x] == piece and \
               board[y][x+1] == piece and \
               board[y][x+2] == piece and \
               board[y][x+3] == piece:
                return True

    for x in range(COLUMN_COUNT):
        for y in range(ROW_COUNT - 3):
            if board[y][x] == piece and \
               board[y+1][x] == piece and \
               board[y+2][x] == piece and \
               board[y+3][x] == piece:
                return True

    for x in range(COLUMN_COUNT - 3):
        for y in range(ROW_COUNT - 3):
            if board[y][x] == piece and \
               board[y+1][x+1] == piece and \
               board[y+2][x+2] == piece and \
               board[y+3][x+3] == piece:
                return True

    for x in range(COLUMN_COUNT - 3):
        for y in range(3, ROW_COUNT):
            if board[y][x] == piece and \
               board[y-1][x+1] == piece and \
               board[y-2][x+2] == piece and \
               board[y-3][x+3] == piece:
                return True

    return False
# Function to let the AI (Player 2) make a random move
def ai_move(board):
    valid_moves = [col for col in range(COLUMN_COUNT) if is_valid(board, col)]
    return random.choice(valid_moves)

# ... (previous code)
def draw_board(board):
    for x in range(COLUMN_COUNT):
        for y in range(ROW_COUNT):
            pygame.draw.rect(screen, BLUE, (x*Square_Size, y*Square_Size+Square_Size, Square_Size, Square_Size))
            pygame.draw.circle(screen, BLACK, (int(x*Square_Size+Square_Size/2), int(y*Square_Size+Square_Size*3/2)), RADIUS)

    for x in range(COLUMN_COUNT):
        for y in range(ROW_COUNT):
            if board[y][x] == 1:
                pygame.draw.circle(screen, RED, (x*Square_Size + Square_Size//2, Height - y*Square_Size - Square_Size//2), RADIUS)
            elif board[y][x] == 2:
                pygame.draw.circle(screen, YELLOW, (x*Square_Size + Square_Size//2, Height - y*Square_Size - Square_Size//2), RADIUS)

    pygame.display.update()

# Initialize Pygame
pygame.init()

Square_Size = 100
Width = COLUMN_COUNT * Square_Size
Height = (ROW_COUNT+1) * Square_Size
size = (Width, Height)
RADIUS = int(Square_Size/2 - 5)

screen = pygame.display.set_mode(size)
board = create_board()  # Create the game board
draw_board(board)

game_over = False
turn = 0

font_create = pygame.font.SysFont("Times New Roman", 75)

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, BLACK, (0, 0, Width, Square_Size))
            pos_x = event.pos[0]
            if turn == 0:
                pygame.draw.circle(screen, RED, (pos_x, int(Square_Size / 2)), RADIUS)
            else:
                pygame.draw.circle(screen, YELLOW, (pos_x, int(Square_Size / 2)), RADIUS)

        pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN and turn == 0:
            pygame.draw.rect(screen, BLACK, (0, 0, Width, Square_Size))
            pos_x = event.pos[0]
            user_option = pos_x // Square_Size

            if is_valid(board, user_option):
                row = get_next_open_row(board, user_option)
                drop_piece(board, row, user_option, 1)
                if winning_board(board, 1):
                    label = font_create.render("Player 1 Wins!!!", 1, RED)
                    screen.blit(label, (40, 10))
                    game_over = True

            print_board(board)
            draw_board(board)
            turn = 1  # Switch to AI's turn

        elif turn == 1 and not game_over:  # AI's turn
            ai_column = ai_move(board)
            if is_valid(board, ai_column):
                row = get_next_open_row(board, ai_column)
                drop_piece(board, row, ai_column, 2)
                if winning_board(board, 2):
                    label = font_create.render("Player 2 (AI) Wins!!!", 1, YELLOW)
                    screen.blit(label, (40, 10))
                    game_over = True

            print_board(board)
            draw_board(board)
            turn = 0  # Switch back to human player's turn

        if game_over:
            pygame.time.wait(30000)
