import random

import numpy as np
import pygame

ROWS = 6
COLUMNS = 8
AI_PIECE = 2
PLAYER_PIECE = 1
DIFFICULTY = 'Easy'
FIRST_TURN = 'AI'
OPPONENT_TYPE = 'AI'

HEIGHT = 0
WIDTH = 0
SQUARE_SIZE = 0
RADIUS = 0

BLUE = (0, 204, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)


def initialize_board(rows, columns):
    """
    Initialize board function\n

    :param rows:Number of rows of the board
    :param columns:
    Number of columns of the board
    :return:
    A matrix with rows lines and columns columns full with zeros.
    """
    return np.zeros((rows, columns))


def valid_column(board, column):
    """
    :param board:represent matrix of the game
    :param column:the column which you want to see if it's valid
    :return: true if the column has empty positions , false if not
    """
    if board[0][column] == 0:
        return True
    return False


def exist_move(board):
    """
    :param board: matrix of game
    :return: true if exist at least one column with at least one position empty, false if doesn't exist
    """
    for i in range(COLUMNS):
        if valid_column(board, i):
            return True
    return False


def row_index(board, column):
    """

    :param board:  matrix of the game
    :param column: index of a column in the matrix
    :return: true if in matrix , column given by parameter have at least one position empty, false if not
    """
    for i in reversed(range(ROWS)):
        if board[i][column] == 0:
            return i
    return -1


def check_winner(board):
    """
    Function to determine if exists a winner of game.

    :param board: represent the matrix of the game
    :return: return the index of player who win, meaning that have 4 in a row with the same color , 0 if a winner
            doesn't exist
    """
    # check for horizontal 4 in a  row
    for row in range(0, ROWS):
        for column in range(0, COLUMNS - 3):
            winner = board[row][column]
            for i in range(column, column + 4):
                if board[row][column] != board[row][i]:
                    winner = 0
            if winner != 0:
                return int(winner)
    # check vertically for 4 in a row
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


def draw_board(screen, board):
    """
    :param screen: window of pygame where to draw
    :param board: matrix of the game
    :return: none
    """
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


def get_random_move(board):
    """
    :param board: matrix of the game
    :return: a random column represent a move of the game
    """
    while 1:
        col = random.randint(0, COLUMNS - 1)
        if valid_column(board, col):
            return col


def get_valid_columns(board):
    """
    Function for calculate the list of the valid columns in game

    :param board: matrix of the game
    :return: list of valid columns where player can move
    """
    valid_columns = []
    for i in range(board.shape[1]):
        if board[0][i] == 0:
            valid_columns.append(i)
    return valid_columns


def score_seq(seq):
    """
    :param seq: list of 4 integers represent a connected 4 position in game
    :return: score of sequence , determined by checking the number of the same piece of the sequence
    """
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
    """
    :param board: Represent the matrix of game
    :return: Score of the board , representing the combinations of connected 4
    """
    score = 0
    for row in range(0, ROWS):
        for column in range(0, COLUMNS - 3):
            seq = board[row][column:column + 4]
            score += score_seq(seq)

    # check vertically for 4 in a row
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
    """
    Minimax algorithm to determine the move of the AI.

    :param board:   Represent matrix of game
    :param depth: Represent the depth where the algorithm to go.
    :param maximing: Represent if the algorithm is maximize or minimize
    :return: The best move which the AI can perform
    """
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


def draw_end_buttons(screen, message):
    """
    Function which draw buttons for back and restart at the end of the game.

    :param screen: Represent the window of pygame where to draw.
    :param message: Represent the message of the end game , which can be Player win , Player lose , or Tie.
    :return: None
    """
    width_buttons = int(WIDTH / 5)
    height_button = int(width_buttons / 2)
    pygame.draw.rect(screen, BLUE, (0, 0, WIDTH, SQUARE_SIZE))
    pygame.draw.rect(screen, WHITE, (10, 10, width_buttons, height_button))
    my_font = pygame.font.SysFont('Comic Sans MS', int(WIDTH / 30))
    message_back = my_font.render('BACK', False, (0, 0, 0))
    text_rect = message_back.get_rect(center=(5 + int(width_buttons / 2), 5 + int(height_button / 2)))
    screen.blit(message_back, text_rect)
    pygame.draw.rect(screen, WHITE, (WIDTH - width_buttons - 10, 10, WIDTH, height_button))
    message_restart = my_font.render('RESTART', False, (0, 0, 0))
    text_rect = message_restart.get_rect(center=(WIDTH - width_buttons / 2 - 5, int(height_button / 2) + 5))
    screen.blit(message_restart, text_rect)

    text_rect = message.get_rect(center=(WIDTH / 2, 10 + int(message.get_height() / 2)))

    screen.blit(message, text_rect)
    pygame.display.update()
    while True:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()

            if ev.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if 10 <= mouse_pos[0] <= width_buttons + 10 and 10 <= mouse_pos[1] <= height_button + 10:
                    pygame.quit()
                    return
                if (WIDTH - width_buttons - 10) <= mouse_pos[0] <= WIDTH and 10 < mouse_pos[1] <= height_button + 10:
                    pygame.quit()
                    game_initialize(ROWS, COLUMNS, OPPONENT_TYPE, DIFFICULTY, FIRST_TURN)
                    return


def start_game_human(turn):
    """
    Function which start the game between two human players.

    :param turn: Represent who player starts.
    :return: None
    """
    board = initialize_board(ROWS, COLUMNS)
    pygame.init()
    size = (WIDTH, HEIGHT)
    screen = pygame.display.set_mode(size)

    draw_board(screen, board)
    game_over = False
    actual_col_hovered = -1
    my_font = pygame.font.SysFont('Comic Sans MS', 30)
    turn_player1 = my_font.render('Player 1 Turn', False, (0, 0, 0))
    turn_player2 = my_font.render('Player 2 Turn', False, (0, 0, 0))
    middle_rect = turn_player1.get_rect(center=(WIDTH / 2, 10 + int(turn_player1.get_height() / 2)))
    while not game_over:
        if not exist_move(board):
            tie_message = my_font.render('Tie', False, (0, 0, 0))
            draw_end_buttons(screen, tie_message)
            break
        if turn == 1:
            screen.blit(turn_player1, middle_rect)
        if turn == 2:
            screen.blit(turn_player2, middle_rect)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.MOUSEMOTION:

                col = int(event.pos[0] / SQUARE_SIZE)
                if col != actual_col_hovered:
                    actual_col_hovered = col
                    pos_x = (int(event.pos[0] / SQUARE_SIZE) * SQUARE_SIZE + int(SQUARE_SIZE / 2))
                    pos_y = int(SQUARE_SIZE * 3 / 4)
                    pygame.draw.rect(screen, BLUE, (0, 0, WIDTH, SQUARE_SIZE))
                    if turn == 1:
                        screen.blit(turn_player1, middle_rect)
                        pygame.draw.circle(screen, RED, (pos_x, pos_y), RADIUS / 2)
                    else:
                        screen.blit(turn_player2, middle_rect)
                        pygame.draw.circle(screen, YELLOW, (pos_x, pos_y), RADIUS / 2)
                    pygame.display.update()
            if event.type == pygame.MOUSEBUTTONDOWN and valid_column(board, actual_col_hovered):
                col = actual_col_hovered
                row = row_index(board, col)
                board[row][col] = turn
                draw_board(screen, board)
                if check_winner(board) == turn:
                    if turn == 1:
                        win_message = my_font.render('Player 1 Win', False, (0, 0, 0))
                    else:
                        win_message = my_font.render('Player 2 Win', False, (0, 0, 0))
                    game_over = True
                    draw_end_buttons(screen, win_message)
                    break
                else:
                    if turn == 1:
                        turn = 2
                    else:
                        turn = 1


def start_game_easy(turn):
    """
    Function which start the game between a human players and AI, which level is easy.AI move random.

    :param turn: Represent which player starts, 1 for human player to start,2 for the AI.
    :return: None
    """
    board = initialize_board(ROWS, COLUMNS)
    pygame.init()
    size = (WIDTH, HEIGHT)
    screen = pygame.display.set_mode(size)

    draw_board(screen, board)
    game_over = False
    actual_col_hovered = -1
    my_font = pygame.font.SysFont('Comic Sans MS', 30)
    message_turn = my_font.render('Your Turn', False, (0, 0, 0))
    middle_rect = message_turn.get_rect(center=(WIDTH / 2, 10 + int(message_turn.get_height() / 2)))
    while not game_over:
        if not exist_move(board):
            tie_message = my_font.render('Tie', False, (0, 0, 0))
            draw_end_buttons(screen, tie_message)
            break
        if turn == 1:
            screen.blit(message_turn, middle_rect)
        if turn == 2:
            move = get_random_move(board)
            row = row_index(board, move)
            board[row][move] = 2
            draw_board(screen, board)
            if check_winner(board) == 2:
                win_message = my_font.render('You LOSE', False, (0, 0, 0))
                draw_end_buttons(screen, win_message)
                break
            else:
                turn = 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.MOUSEMOTION:
                if turn == 1:
                    col = int(event.pos[0] / SQUARE_SIZE)
                    if col != actual_col_hovered:
                        actual_col_hovered = col
                        pos_x = (int(event.pos[0] / SQUARE_SIZE) * SQUARE_SIZE + int(SQUARE_SIZE / 2))
                        pos_y = int(SQUARE_SIZE * 3 / 4)
                        pygame.draw.rect(screen, BLUE, (0, 0, WIDTH, SQUARE_SIZE))
                        screen.blit(message_turn, middle_rect)
                        pygame.draw.circle(screen, RED, (pos_x, pos_y), RADIUS / 2)
                        pygame.display.update()
            if event.type == pygame.MOUSEBUTTONDOWN and valid_column(board, actual_col_hovered):
                if turn == 1:
                    col = actual_col_hovered
                    row = row_index(board, col)
                    board[row][col] = 1
                    draw_board(screen, board)
                    if check_winner(board) == 1:
                        win_message = my_font.render('You Win', False, (0, 0, 0))
                        game_over = True
                        draw_end_buttons(screen, win_message)
                        break
                    else:
                        turn = 2


def start_game_medium(turn):
    """
        Function which start the game between a human players and AI, which level is medium.AI has a good move
        calculated with minimax , and another which calculate the score of the board.

        :param turn: Represent which player starts, 1 for human player to start,2 for the AI.
        :return: None
        """
    board = initialize_board(ROWS, COLUMNS)
    pygame.init()
    size = (WIDTH, HEIGHT)
    screen = pygame.display.set_mode(size)

    draw_board(screen, board)
    game_over = False
    actual_col_hovered = -1
    my_font = pygame.font.SysFont('Comic Sans MS', 30)
    message_turn = my_font.render('Your Turn', False, (0, 0, 0))
    middle_rect = message_turn.get_rect(center=(WIDTH / 2, 10 + int(message_turn.get_height() / 2)))
    move_type = 1  # 1 means weak move , 2 means strong move
    while not game_over:
        if not exist_move(board):
            tie_message = my_font.render('Tie', False, (0, 0, 0))
            draw_end_buttons(screen, tie_message)
            break
        if turn == 1:
            screen.blit(message_turn, middle_rect)
        if turn == 2:
            if move_type == 1:
                move = minimax(board, 1, True)
                move_type = 2
            else:
                move = minimax(board, 3, True)
                move_type = 1
            col = move[0]
            row = row_index(board, col)
            board[row][col] = 2
            draw_board(screen, board)
            if check_winner(board) == 2:
                win_message = my_font.render('You LOSE', False, (0, 0, 0))

                draw_end_buttons(screen, win_message)
                break
            else:
                turn = 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.MOUSEMOTION:
                if turn == 1:
                    col = int(event.pos[0] / SQUARE_SIZE)
                    if col != actual_col_hovered:
                        actual_col_hovered = col
                        pos_x = (int(event.pos[0] / SQUARE_SIZE) * SQUARE_SIZE + int(SQUARE_SIZE / 2))
                        pos_y = int(SQUARE_SIZE * 3 / 4)
                        pygame.draw.rect(screen, BLUE, (0, 0, WIDTH, SQUARE_SIZE))
                        screen.blit(message_turn, middle_rect)
                        pygame.draw.circle(screen, RED, (pos_x, pos_y), RADIUS / 2)
                        pygame.display.update()
            if event.type == pygame.MOUSEBUTTONDOWN and valid_column(board, actual_col_hovered):
                if turn == 1:
                    col = actual_col_hovered
                    row = row_index(board, col)
                    board[row][col] = 1
                    draw_board(screen, board)
                    if check_winner(board) == 1:
                        win_message = my_font.render('You Win', False, (0, 0, 0))
                        game_over = True
                        draw_end_buttons(screen, win_message)
                        break
                    else:
                        turn = 2


def start_game_hard(turn):
    """
     Function which start the game between a human players and AI, which level is HARD.AI move by using the minimax
     algorithm only.

    :param turn: Represent which player starts, 1 for human player to start,2 for the AI.
    :return: None
    """
    board = initialize_board(ROWS, COLUMNS)
    pygame.init()
    size = (WIDTH, HEIGHT)
    screen = pygame.display.set_mode(size)

    draw_board(screen, board)
    game_over = False
    actual_col_hovered = -1
    my_font = pygame.font.SysFont('Comic Sans MS', int(WIDTH / 25))
    message_turn = my_font.render('Your Turn', False, (0, 0, 0))
    middle_rect = message_turn.get_rect(center=(WIDTH / 2, 10 + int(message_turn.get_height() / 2)))
    while not game_over:
        if not exist_move(board):
            tie_message = my_font.render('Tie', False, (0, 0, 0))
            draw_end_buttons(screen, tie_message)
            break
        if turn == 1:
            screen.blit(message_turn, middle_rect)
            pygame.display.update()
        if turn == 2:
            move = minimax(board, 3, True)
            col = move[0]
            row = row_index(board, col)
            board[row][col] = 2
            draw_board(screen, board)
            if check_winner(board) == 2:
                win_message = my_font.render('You LOSE', False, (0, 0, 0))
                draw_end_buttons(screen, win_message)
                break
            else:
                turn = 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.MOUSEMOTION:
                if turn == 1:
                    col = int(event.pos[0] / SQUARE_SIZE)
                    if col != actual_col_hovered:
                        actual_col_hovered = col
                        pos_x = (int(event.pos[0] / SQUARE_SIZE) * SQUARE_SIZE + int(SQUARE_SIZE / 2))
                        pos_y = int(SQUARE_SIZE * 3 / 4)
                        pygame.draw.rect(screen, BLUE, (0, 0, WIDTH, SQUARE_SIZE))
                        screen.blit(message_turn, middle_rect)
                        pygame.draw.circle(screen, RED, (pos_x, pos_y), RADIUS / 2)
                        pygame.display.update()
            if event.type == pygame.MOUSEBUTTONDOWN and valid_column(board, actual_col_hovered):
                if turn == 1:
                    col = actual_col_hovered
                    row = row_index(board, col)
                    board[row][col] = 1
                    draw_board(screen, board)
                    if check_winner(board) == 1:
                        win_message = my_font.render('You Win', False, (0, 0, 0))
                        game_over = True
                        draw_end_buttons(screen, win_message)
                        break
                    else:
                        turn = 2


def game_initialize(rows, columns, opponent_type, difficulty, start):
    """
    Function which initialize the game parameters and starts it.

    :param rows: Represent number of rows of the game.
    :param columns: Represent number of columns of the game.
    :param opponent_type: Represent the opponent type , AI or Human.
    :param difficulty: Represent the difficulty if we play with the AI.
    :param start: Represent which player starts , AI or Human.
    :return: None
    """
    global ROWS
    ROWS = int(rows)
    global COLUMNS
    COLUMNS = int(columns)
    global OPPONENT_TYPE
    OPPONENT_TYPE = opponent_type
    global DIFFICULTY
    DIFFICULTY = difficulty
    global FIRST_TURN
    FIRST_TURN = start
    global SQUARE_SIZE
    global RADIUS
    SQUARE_SIZE = 100
    RADIUS = int(SQUARE_SIZE / 2) - 10
    if ROWS >= 7:
        SQUARE_SIZE = 80
        RADIUS = int(SQUARE_SIZE / 2) - 10
    if ROWS >= 10:
        SQUARE_SIZE = 60
        RADIUS = int(SQUARE_SIZE / 2) - 10

    global HEIGHT
    HEIGHT = ROWS * SQUARE_SIZE + 100
    global WIDTH
    WIDTH = COLUMNS * SQUARE_SIZE
    if opponent_type == 'AI':
        if difficulty == 'Easy':
            if start == 'AI':
                start_game_easy(2)
            else:
                start_game_easy(1)
        elif difficulty == 'Medium':
            if start == 'AI':
                start_game_medium(2)
            else:
                start_game_medium(1)
        elif difficulty == 'Hard':
            if start == 'AI':
                start_game_hard(2)
            else:
                start_game_hard(1)
    else:
        start_game_human(1)
