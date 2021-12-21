import random
import time

import numpy as np
import pygame
import sys
import math

ROWS = 6
COLUMNS = 8
AI_PIECE = 2
PLAYER_PIECE = 1


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
    return -1


SQUARE_SIZE = 100
BLUE = (0, 204, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
HEIGHT = ROWS * SQUARE_SIZE + 100
WIDTH = COLUMNS * SQUARE_SIZE
RADIUS = int(SQUARE_SIZE / 2) - 10


def draw_board(screen, board):
    screen.fill(BLUE)

    for i in range(0, ROWS):
        for j in range(0, COLUMNS):
            pos = (int(j * SQUARE_SIZE + SQUARE_SIZE / 2), SQUARE_SIZE + int(i * SQUARE_SIZE + SQUARE_SIZE / 2))
            pygame.draw.circle(screen, WHITE, pos, RADIUS)

    for i in range(ROWS):
        for j in range(COLUMNS):
            if board[i][j] == 1:
                pos = (int(j * SQUARE_SIZE + SQUARE_SIZE / 2), SQUARE_SIZE + int(i * SQUARE_SIZE + SQUARE_SIZE / 2))
                pygame.draw.circle(screen, RED, pos, RADIUS)
            elif board[i][j] == 2:
                pos = (int(j * SQUARE_SIZE + SQUARE_SIZE / 2), SQUARE_SIZE + int(i * SQUARE_SIZE + SQUARE_SIZE / 2))
                pygame.draw.circle(screen, YELLOW, pos, RADIUS)
    pygame.display.update()


game_over = False
turn = 1


def get_random_move(board):
    while 1:
        col = random.randint(0, COLUMNS - 1)
        if valid_column(board, col):
            return col
    return 0


def get_valid_columns(board):
    valid_columns = []
    for i in range(board.shape[1]):
        if board[0][i] == 0:
            valid_columns.append(i)
    return valid_columns


def score_seq(seq):
    if np.count_nonzero(seq == AI_PIECE) == 4:
        return 100
    if np.count_nonzero(seq == PLAYER_PIECE) == 4:
        return -100
    if np.count_nonzero(seq == AI_PIECE) == 3 and np.count_nonzero(seq == 0) == 1:
        return 10
    if np.count_nonzero(seq == PLAYER_PIECE) == 3 and np.count_nonzero(seq == 0) == 1:
        return -10
    if np.count_nonzero(seq == AI_PIECE) == 2 and np.count_nonzero(seq == 0) == 2:
        return 5
    if np.count_nonzero(seq == PLAYER_PIECE) == 2 and np.count_nonzero(seq == 0) == 2:
        return -5
    return 0


def evaluate_board(board):
    score = 0
    for row in range(0, ROWS):
        for column in range(0, COLUMNS - 3):
            seq = board[row][column:column + 4]
            score += score_seq(seq)

    # check verticaly for 4 in a row
    for row in range(0, ROWS - 3):

        for column in range(0, COLUMNS):

            seq = []
            for i in range(0, 4):
                seq.append(board[row + i][column])
            score += score_seq(seq)

    for row in range(0, ROWS - 3):
        for column in range(0, COLUMNS - 3):
            seq = []
            for i in range(0, 4):
                seq.append(board[row + i][column + i])
            score += score_seq(seq)

    for row in range(0, ROWS - 3):
        for column in range(3, COLUMNS):

            seq = []
            for i in range(0, 4):
                seq.append(board[row + i][column - i])
            score += score_seq(seq)
    return score


def minimax(board, depth, maximing: bool):
    winner = check_winner(board)
    if winner == AI_PIECE:
        return None, 100
    if winner == PLAYER_PIECE:
        return None, -100
    if depth == 0:
        return None, evaluate_board(board)

    if maximing:
        score = -500
        valid_columns = get_valid_columns(board)
        best_column = random.choice(valid_columns)
        if valid_columns == 0:
            return 0
        for col in valid_columns:
            row = row_index(board, col)
            board_modify = board.copy()
            board_modify[row][col] = AI_PIECE
            score_move = minimax(board_modify, depth - 1, not maximing)[1]

            if score_move > score:
                score = score_move
                best_column = col

        return best_column, score

    else:
        score = 500
        valid_columns = get_valid_columns(board)
        best_column = random.choice(valid_columns)
        if valid_columns == 0:
            return 0
        for col in valid_columns:
            row = row_index(board, col)
            board_modify = board.copy()
            board_modify[row][col] = PLAYER_PIECE
            score_move = minimax(board_modify, depth - 1, not maximing)[1]
            if score_move < score:
                score = score_move
                best_column = col
        return best_column, score


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

            move = minimax(board, 3, True)
            col = move[0]
            row = row_index(board, col)
            board[row][col] = 2

            draw_board(screen, board)
            if check_winner(board) == 2:
                win_message = my_font.render('You LOSEEEEE', False, (0, 0, 0))
                pygame.draw.rect(screen, BLUE, (0, 0, WIDTH, SQUARE_SIZE))
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
                    col = int(event.pos[0] / SQUARE_SIZE)
                    if col != actual_real:
                        actual_real = col
                        pos_x = (int(event.pos[0] / SQUARE_SIZE) * SQUARE_SIZE + int(SQUARE_SIZE / 2))
                        pos_y = int(SQUARE_SIZE * 3 / 4)
                        pygame.draw.rect(screen, BLUE, (0, 0, WIDTH, SQUARE_SIZE))
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
                        win_message = my_font.render('You Win', False, (0, 0, 0))
                        pygame.draw.rect(screen, BLUE, (0, 0, WIDTH, SQUARE_SIZE))
                        screen.blit(win_message, (0, 0))
                        pygame.display.update()
                        turn = 0
                    else:
                        turn = 2


def game_initialize(rows, columns, opponent_type, dificulty, start):
    global ROWS
    ROWS = int(rows)
    global COLUMNS
    COLUMNS = int(columns)

    global SQUARE_SIZE
    global RADIUS
    if ROWS >= 7:
        SQUARE_SIZE = 80
        RADIUS = int(SQUARE_SIZE / 2) - 10
    global HEIGHT
    HEIGHT = ROWS * SQUARE_SIZE + 100
    global WIDTH
    WIDTH = COLUMNS * SQUARE_SIZE
    if opponent_type == 'AI':
        start_game()
