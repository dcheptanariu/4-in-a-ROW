import random
import time

import numpy as np
import pygame
import sys
import math

ROWS = 5
COLUMNS = 8


def initialize_board(rows, columns):
    return np.zeros((rows, columns))


def read_settings():
    global ROWS
    ROWS = int(input("Enter number of rows: "))
    global COLUMNS
    COLUMNS = int(input("Enter number of columns:"))


def valid_column(board, column):
    if board[0][column] == 0:
        return True
    return False


def set_piece(board, column, color):
    row = row_index(board, column)
    if row >= 0:
        board[row][column] = color


def row_index(board, column):
    for i in reversed(range(ROWS)):
        if board[i][column] == 0:
            return i
    return -1


def check_winner(board):
    winner = 0
    # check for horizontall 4 in a  row
    for row in range(0, ROWS):
        for column in range(0, COLUMNS - 3):
            winner = board[row][column]
            for i in range(column, column + 4):
                if board[row][column] != board[row][i]:
                    winner = 0
            if winner != 0:
                return int(winner)
    # check verticaly for 4 in a row
    for row in range(0, ROWS - 3):

        for column in range(0, COLUMNS):
            winner = board[row][column]
            for i in range(row, row + 4):
                if board[row][column] != board[i][column]:
                    winner = 0
            if winner != 0:
                return int(winner)
    for row in range(0, ROWS - 3):
        for column in range(0, COLUMNS - 3):
            winner = board[row][column]
            for i in range(0, 4):
                if winner != board[row + i][column + i]:
                    winner = 0
            if winner != 0:
                return int(winner)

    for row in range(0, ROWS - 3):
        for column in range(3, COLUMNS):
            winner = board[row][column]
            for i in range(0, 4):
                if winner != board[row + i][column - i]:
                    winner = 0
            if winner != 0:
                return int(winner)


SQUARESIZE = 100
BLUE = (0, 204, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
HEIGHT = ROWS * SQUARESIZE + 100
WIDTH = COLUMNS * SQUARESIZE
RADIUS = int(SQUARESIZE / 2) - 10


def draw_board(screen, board):
    screen.fill(BLUE)

    for i in range(0, ROWS):
        for j in range(0, COLUMNS):
            pos = (int(j * SQUARESIZE + SQUARESIZE / 2), SQUARESIZE + int(i * SQUARESIZE + SQUARESIZE / 2))
            pygame.draw.circle(screen, WHITE, pos, RADIUS)

    for i in range(ROWS):
        for j in range(COLUMNS):
            if board[i][j] == 1:
                pos = (int(j * SQUARESIZE + SQUARESIZE / 2), SQUARESIZE + int(i * SQUARESIZE + SQUARESIZE / 2))
                pygame.draw.circle(screen, RED, pos, RADIUS)
            elif board[i][j] == 2:
                pos = (int(j * SQUARESIZE + SQUARESIZE / 2), SQUARESIZE + int(i * SQUARESIZE + SQUARESIZE / 2))
                pygame.draw.circle(screen, YELLOW, pos, RADIUS)
    pygame.display.update()


pygame.init()
size = (WIDTH, HEIGHT)
screen = pygame.display.set_mode(size)


game_over = False
turn = 1


def get_random_move(board):
    while 1:
        col = random.randint(0, COLUMNS-1)
        if valid_column(board, col):
            return col
    return 0


def start_game():
    board = initialize_board(ROWS, COLUMNS)
    pygame.init()
    size = (WIDTH, HEIGHT)
    screen = pygame.display.set_mode(size)

    draw_board(screen, board)
    game_over = False
    turn = 1
    actual_real = -1
    my_font = pygame.font.SysFont('Comic Sans MS', 30)
    message_turn = my_font.render('Your Turn', False, (0, 0, 0))
    while not game_over:
        if turn == 1:
            screen.blit(message_turn, (0, 0))
        if turn == 2:
            col=get_random_move(board)
            row = row_index(board, col)
            board[row][col] = 2
            print(board)
            draw_board(screen, board)
            if check_winner(board) == 2:
                win_message = my_font.render('You LOSEEEEE', False, (0, 0, 0))
                pygame.draw.rect(screen, BLUE, (0, 0, WIDTH, SQUARESIZE))
                screen.blit(win_message, (0, 0))
                pygame.display.update()
                turn = 0
            else:
                turn = 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEMOTION:
                if turn == 1:
                    col = int(event.pos[0] / SQUARESIZE)
                    if col != actual_real:
                        actual_real = col
                        pos_x = (int(event.pos[0] / SQUARESIZE) * SQUARESIZE + int(SQUARESIZE / 2))
                        pos_y = int(SQUARESIZE * 3 / 4)
                        pygame.draw.rect(screen, BLUE, (0, 0, WIDTH, SQUARESIZE))
                        screen.blit(message_turn, (0, 0))
                        print(pos_x, pos_y)
                        pygame.draw.circle(screen, RED, (pos_x, pos_y), RADIUS / 2)
                        pygame.display.update()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if (turn == 1):
                    col = actual_real
                    row = row_index(board, col)
                    board[row][col] = 1
                    draw_board(screen, board)
                    if check_winner(board) == 1:
                        win_message=my_font.render('You Win', False, (0, 0, 0))
                        pygame.draw.rect(screen, BLUE, (0, 0, WIDTH, SQUARESIZE))
                        screen.blit(win_message, (0, 0))
                        pygame.display.update()
                        turn=0
                    else:
                        turn = 2


start_game()
