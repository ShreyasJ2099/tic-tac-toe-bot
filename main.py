# Setup
import copy
import os
import random
import time

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide'

import pygame

pygame.init()
window = pygame.display.set_mode((300, 300))
pygame.display.set_caption('Tic Tac Toe')
os.system('clear')

width = window.get_width()
space = width / 30
size = (width - 2 * space) / 3
running = True

player1 = True
player2 = False

turn = 0
place = ['O', 'X']
players = ['Player 1 (O)', 'Player 2 (X)']

moveLog = []

# Classes
class Square:
    def __init__(self, value, position, image):
        self.value = value
        self.position = position
        self.image = image

# Functions
def print_grid():
    for y in range(3):
        for x in range(3):
            print(grid[y][x].value, end = ' ')
        print()

def draw_shape(shape, y, x):
    if shape == 'O':
        pygame.draw.circle(window, (50, 225, 255), (x, y), size * 2 / 5, width = 10)
    elif shape == 'X':
        font = pygame.font.SysFont('Sans', 80, bold = True)
        shape = font.render('X', True, (255, 78, 152))
        window.blit(shape, (x - (size / 3), y - (size / 2)))

def draw_grid():
    for y in range(3):
        for x in range(3):
            i = grid[y][x].image

def draw_values():
    for y in range(3):
        for x in range(3):
            if grid[y][x].value != ' ':
                drawY = (y * size) + (y * space) + (size / 2)
                drawX = (x * size) + (x * space) + (size / 2)
                draw_shape(grid[y][x].value, drawY, drawX)

def highlight_square():
    if (turn == 0 and player1) or (turn == 1 and player2):
        for y in range(3):
            for x in range(3):
                if grid[y][x].image.collidepoint(pygame.mouse.get_pos()):
                    grid[y][x].image = pygame.draw.rect(window, (220, 255, 180), (x * (size + space), y * (size + space), size, size))
                else:
                    grid[y][x].image = pygame.draw.rect(window, (255, 255, 255), (x * (size + space), y * (size + space), size, size))

def sense_win(grid):
    if grid[0][0].value == grid[0][1].value == grid[0][2].value and grid[0][0].value != ' ':
        return grid[0][0].value
    elif grid[1][0].value == grid[1][1].value == grid[1][2].value and grid[1][0].value != ' ':
        return grid[1][0].value
    elif grid[2][0].value == grid[2][1].value == grid[2][2].value and grid[2][0].value != ' ':
        return grid[2][0].value
    elif grid[0][0].value == grid[1][0].value == grid[2][0].value and grid[0][0].value != ' ':
        return grid[0][0].value
    elif grid[0][1].value == grid[1][1].value == grid[2][1].value and grid[0][1].value != ' ':
        return grid[0][1].value
    elif grid[0][2].value == grid[1][2].value == grid[2][2].value and grid[0][2].value != ' ':
        return grid[0][2].value
    elif grid[0][0].value == grid[1][1].value == grid[2][2].value and grid[0][0].value != ' ':
        return grid[0][0].value
    elif grid[0][2].value == grid[1][1].value == grid[2][0].value and grid[0][2].value != ' ':
        return grid[0][2].value
    else:
        return None

def sense_draw(grid):
    return sense_win(grid) is None and grid_is_full(grid) 

def get_empty(grid):
    empty = []
    for y in range(3):
        for x in range(3):
            if grid[y][x].value == ' ':
                empty.append((y, x))
    return empty

def game_over(winner):
    pygame.display.update()
    time.sleep(3)
    font2 = pygame.font.SysFont('Sans', round(width / 12))
    if winner != '':    
        text = font2.render(winner + ' wins!', False, (255, 255, 255))
    else:
        text = font2.render("It is a draw.", False, (255, 255, 255))
    window.fill((0, 0, 0))
    window.blit(text, (width / 8, width / 2))
    pygame.display.update()

def make_random(grid):
    if (not grid_is_full(grid)):
        set = False
        time.sleep(1)
        while not set:
            y, x = random.randint(0, 2), random.randint(0, 2)
            if grid[y][x].value == ' ':
                grid[y][x].value = place[turn]
                set = True
        return grid

def make_best(grid):
    global turn
    score, move = AI(grid, place[turn], 1, -10, 10)
    print(f'AI chose move {move} with an eval of {score}.')
    if move is not None:
        y, x = move
        grid[y][x].value = place[turn]
        moveLog.append((place[turn], move))

def AI(board, goal, mod, alpha, beta):
    empty = get_empty(board)
    best_score = -10 * mod
    best_move = None
    goal_index = place.index(goal)
    # Terminal Cases
    if sense_win(board) is not None:
        if sense_win(board) == goal:
            return 1 * mod, best_move
        elif sense_win(board) != goal:
            return -1 * mod, best_move
    elif sense_draw(board):
        return 0, best_move
    # Recursions
    for (y, x) in empty:
        temp = copy.deepcopy(board)
        temp[y][x].value = goal
        score, move = AI(temp, place[1 - goal_index], -1 * mod, alpha, beta)
        if mod == 1:
            if score > best_score:
                best_score = score
                best_move = (y, x)
            alpha = max(alpha, best_score)
        elif mod == -1 and score < best_score:
            best_score = score
            best_move = (y, x)
            beta = min(beta, best_score)
        if alpha >= beta:
            break
    # return result
    return best_score, best_move

def grid_is_full(grid):
    full = True
    for row in grid:
        for item in row:
            if item.value == ' ':
                full = False
    return full

# On start
TL = Square(' ', (0, 0), pygame.draw.rect(window, (255, 255, 255), (0 * (size + space), 0 * (size + space), size, size)))
TM = Square(' ', (0, 1), pygame.draw.rect(window, (255, 255, 255), (1 * (size + space), 0 * (size + space), size, size)))
TR = Square(' ', (0, 2), pygame.draw.rect(window, (255, 255, 255), (2 * (size + space), 0 * (size + space), size, size)))
ML = Square(' ', (1, 0), pygame.draw.rect(window, (255, 255, 255), (0 * (size + space), 1 * (size + space), size, size)))
MM = Square(' ', (1, 1), pygame.draw.rect(window, (255, 255, 255), (1 * (size + space), 1 * (size + space), size, size)))
MR = Square(' ', (1, 2), pygame.draw.rect(window, (255, 255, 255), (2 * (size + space), 1 * (size + space), size, size)))
BL = Square(' ', (2, 0), pygame.draw.rect(window, (255, 255, 255), (0 * (size + space), 2 * (size + space), size, size)))
BM = Square(' ', (2, 1), pygame.draw.rect(window, (255, 255, 255), (1 * (size + space), 2 * (size + space), size, size)))
BR = Square(' ', (2, 2), pygame.draw.rect(window, (255, 255, 255), (2 * (size + space), 2 * (size + space), size, size)))

grid = [
    [TL, TM, TR], 
    [ML, MM, MR],
    [BL, BM, BR]
]

while running:
    draw_grid()
    highlight_square()
    draw_values()
    pygame.display.update() 
    if sense_win(grid) is not None:
        game_over(players[place.index(sense_win(grid))])
        break

    elif sense_win(grid) is None and grid_is_full(grid):
        game_over('')
        break
    # Run AI
    if ((turn == 0 and not player1) or (turn == 1 and not player2)):
        make_best(grid)
        turn = 1 - turn
    # Events
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN and ((turn == 0 and player1) or (turn == 1 and player2)):
            for y in range(3):
                for x in range(3):
                    if grid[y][x].image.collidepoint(pygame.mouse.get_pos()) and grid[y][x].value == ' ':
                        grid[y][x].value = place[turn]
                        moveLog.append((place[turn], (y, x)))
                        turn = 1 - turn

while True:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN and event.key == pygame.K_l:
            os.system('clear')
            print(moveLog)
