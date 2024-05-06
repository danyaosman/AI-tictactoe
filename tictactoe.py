import sys
import pygame
import numpy as np
import random
import copy
from constants import *

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("tictactoe ai")
screen.fill(BG_COLOUR)

class Board:

    def __init__(self):
        self.squares = np.zeros((ROWS, COLS))
        self.empty_squares = self.squares
        self.marked_squares = 0

    def final_state(self):
        #check rows
        for row in range(ROWS):
            if self.squares[row][0] == self.squares[row][1] == self.squares[row][2] != 0:
                return self.squares[row][0]
        #check columns
        for col in range(COLS):
            if self.squares[0][col] == self.squares[1][col] == self.squares[2][col] != 0:
                return self.squares[0][col]
        #check diagonals
        if self.squares[0][0] == self.squares[1][1] == self.squares[2][2] != 0:
            return self.squares[0][0]
        if self.squares[0][2] == self.squares[1][1] == self.squares[2][0] != 0:
            return self.squares[0][2]
        
        return 0

    def mark_square(self, row, col, player):
        self.squares[row][col] = player
        self.marked_squares += 1

    def is_square_empty(self, row, col):
        return self.squares[row][col] == 0
    
    def get_empty_squares(self):
        empty_squares = []
        for row in range(ROWS):
            for col in range(COLS):
                if self.is_square_empty(row, col):
                    empty_squares.append((row, col))
        return empty_squares
    
    def isfull(self):
        return self.marked_squares == ROWS * COLS
    
    def isempty(self):
        return self.marked_squares == 0

class AI:
    
    def __init__(self, level=1, player=2):
        self.level = level
        self.player = player

    def rnd(self, board):
        empty_squares = board.get_empty_squares()
        index = random.randrange(0, len(empty_squares))
        return empty_squares[index]
    
    def minimax(self,board,maximising):
        case = board.final_state()

        #p1 wins
        if case == 1:
            return 1, None #eval move
        
        #p2 wins
        if case == 2:
            return -1, None #eval move
        
        elif board.isfull():
            return 0, None #eval move
        
        if maximising:
            max_eval = -999
            best_move = None
            empty_squares = board.get_empty_squares()

            for (row, col) in empty_squares:
                temp_board = copy.deepcopy(board)
                temp_board.mark_square(row, col, 1)
                eval = self.minimax(temp_board, False)[0]
                if eval > max_eval:
                    max_eval = eval
                    best_move = (row, col)
                    
            return max_eval, best_move

        elif not maximising:
            min_eval = 999
            best_move = None
            empty_squares = board.get_empty_squares()

            for (row, col) in empty_squares:
                temp_board = copy.deepcopy(board)
                temp_board.mark_square(row, col, self.player)
                eval = self.minimax(temp_board, True)[0]
                if eval < min_eval:
                    min_eval = eval
                    best_move = (row, col)

            return min_eval, best_move


    def eval(self, main_board):
        if self.level == 0:
            #random
            eval = 'random'
            move = self.rnd(main_board)

        else:
            #minimax
            eval, move = self.minimax(main_board, False)

        print(f'AI has chosen to mark the square in pos {move} with an evalualiton of {eval}')
        
        return move

class Game:

    def __init__(self):
        self.board = Board()
        self.ai = AI()
        self.player = 1
        self.gamemode = 'ai'
        self.running = True
        self.show_lines()

    def make_move(self, row, col):
        self.board.mark_square(row, col, self.player)
        self.draw_fig(row, col)
        self.next_turn()

    def show_lines(self):
        screen.fill(BG_COLOUR)
        #vertical lines
        pygame.draw.line(screen, LINE_COLOUR, (SQSIZE, 0), (SQSIZE, HEIGHT), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOUR, (WIDTH-SQSIZE, 0), (WIDTH - SQSIZE, HEIGHT), LINE_WIDTH)
        #horizontal
        pygame.draw.line(screen, LINE_COLOUR, (0, SQSIZE), (WIDTH, SQSIZE), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOUR, (0, HEIGHT-SQSIZE), (WIDTH, HEIGHT-SQSIZE), LINE_WIDTH)

    def next_turn(self):
        self.player = self.player%2 + 1

    def draw_fig(self, row, col):
        if self.player == 1:
            #desc line
            start_desc = (col*SQSIZE + OFFSET, row*SQSIZE + OFFSET)
            end_desc = ((col+1)*SQSIZE - OFFSET, (row+1)*SQSIZE - OFFSET)
            pygame.draw.line(screen, CROSS_COLOUR, start_desc, end_desc, CROSS_WIDTH)
            #asc line
            start_asc = ((col+1)*SQSIZE - OFFSET, row*SQSIZE + OFFSET)
            end_asc = (col*SQSIZE + OFFSET, (row+1)*SQSIZE - OFFSET)
            pygame.draw.line(screen, CROSS_COLOUR, start_asc, end_asc, CROSS_WIDTH)

        elif self.player == 2:
            center = (col * SQSIZE + SQSIZE//2, row * SQSIZE + SQSIZE//2)
            pygame.draw.circle(screen, CIRCLE_COLOUR, center, RADIUS, CIRCLE_WIDTH)
    
    def change_gamemode(self):
        self.gamemode = 'ai' if self.gamemode == 'pvp' else 'pvp'

    def over(self):
        if self.board.final_state() != 0:
            print(f'Player {self.board.final_state()} wins!')
            return True
        elif self.board.isfull():
            print('Tie!')
            return True
        return False

    def reset(self):
        self.__init__()

def main():

    #object
    game = Game()
    board = game.board
    ai = game.ai

    #mainloop
    while True:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                row = pos[1] // SQSIZE
                col = pos[0] // SQSIZE

                if (board.is_square_empty(row, col)) and game.running:
                    game.make_move(row, col)
                    if game.over():
                        game.running = False


            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_r:
                    game.reset()
                    board = game.board
                    ai = game.ai

                if event.key == pygame.K_g:
                    game.change_gamemode()

                #change ai to random
                if event.key == pygame.K_0:
                    ai.level = 0

                #change ai to minimax
                if event.key == pygame.K_1:
                    ai.level = 1

        if game.gamemode == 'ai' and game.player == ai.player and game.running:
            pygame.display.update()

            #ai methods
            row, col = ai.eval(board)

            game.make_move(row, col)
            if game.over():
                game.running = False

        pygame.display.update()

main()