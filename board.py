import pygame
from sudoku_generator import SudokuGenerator
from cell import Cell

class Board:
    def __init__(self, width, height, screen, difficulty):
        self.width, self.height, self.screen = width, height, screen
        self.removed = {"easy": 30, "medium": 40, "hard": 50}[difficulty]
        
        # Manual steps to preserve the solution
        self.gen = SudokuGenerator(9, self.removed)
        self.gen.fill_values()
        self.solution = self.gen.get_board()
        self.gen.remove_cells()
        self.initial_board = self.gen.get_board()
        
        self.cells = [[Cell(self.initial_board[i][j], i, j, screen) for j in range(9)] for i in range(9)]
        self.selected_row, self.selected_col = 0, 0
        self.cells[0][0].selected = True

    def draw(self):
        for i in range(10):
            thick = 4 if i % 3 == 0 else 1
            pygame.draw.line(self.screen, (0,0,0), (0, i*60), (540, i*60), thick)
            pygame.draw.line(self.screen, (0,0,0), (i*60, 0), (i*60, 540), thick)
        for row in self.cells:
            for cell in row: cell.draw()

    def select(self, row, col):
        self.cells[self.selected_row][self.selected_col].selected = False
        self.selected_row, self.selected_col = row, col
        self.cells[row][col].selected = True

    def click(self, x, y):
        return (y // 60, x // 60) if 0 <= x < 540 and 0 <= y < 540 else None

    def sketch(self, value):
        if self.initial_board[self.selected_row][self.selected_col] == 0:
            self.cells[self.selected_row][self.selected_col].set_sketched_value(value)

    def place_number(self, value):
        if self.initial_board[self.selected_row][self.selected_col] == 0:
            self.cells[self.selected_row][self.selected_col].set_cell_value(value)

    def reset_to_original(self):
        for i in range(9):
            for j in range(9):
                self.cells[i][j].set_cell_value(self.initial_board[i][j])
                self.cells[i][j].set_sketched_value(0)

    def is_full(self):
        return all(cell.value != 0 for row in self.cells for cell in row)

    def check_board(self):
        return all(self.cells[i][j].value == self.solution[i][j] for i in range(9) for j in range(9))