import numpy as np
import pygame
import sys
import math

rows = 0
columns = 0


def initialize_board():
    return np.zeros((rows, columns))


def read_settings():
    global rows
    rows = int(input("Enter number of rows: "))
    global columns
    columns = int(input("Enter number of columns:"))


def valid_column(column):
    if board[columns - 1][column] == 0:
        return True
    return False


def set_piece(column, color):
    board[row_index(column)][column] = color


def row_index(column):
    for i in range(rows):
        if board[i][column] > 0:
            return i - 1
    return rows - 1


def check_winner():
    winner = 0
    # check for horizontall 4 in a  row
    for row in range(0, rows):
        for column in range(0, columns - 3):
            winner = board[row][column]
            for i in range(column, column + 4):
                if board[row][column] != board[row][i]:
                    winner = 0
            if winner != 0:
                return int(winner)
    # check verticaly for 4 in a row
    for row in range(0, rows - 3):
        for column in range(0, columns):
            winner = board[row][column]
            for i in range(row, row + 4):
                if board[row][column] != board[i][column]:
                    winner = 0

            if winner != 0:
                print(winner)
                return int(winner)


read_settings()
board = initialize_board()

board[1][1] = 1
board[2][1] = 1
board[3][1] = 1
board[4][1] = 1
check_winner()
