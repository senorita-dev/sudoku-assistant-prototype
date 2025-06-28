from sudoku import Sudoku, sys
from random import randrange
import sys
from type_defs import Board, Step, SudokuData, TypedDict


def empty_board() -> Board:
    return [[None for _ in range(9)] for _ in range(9)]


def copy_board(board: Board) -> Board:
    return [row.copy() for row in board]


def transpose(board: Board) -> Board:
    new_board = empty_board()
    for rowIndex, row in enumerate(board):
        for colIndex, cell in enumerate(row):
            new_board[rowIndex][colIndex] = board[colIndex][rowIndex]
    return new_board


def get_square(board: Board, y: int, x: int) -> list[int | None]:
    min_y = (y // 3) * 3
    max_y = (y // 3) * 3 + 3
    min_x = (x // 3) * 3
    max_x = (x // 3) * 3 + 3
    return [
        board[curr_y][curr_x]
        for curr_x in range(min_x, max_x)
        for curr_y in range(min_y, max_y)
    ]


class SudokuManager:
    def __init__(self):
        self.puzzle: Board = Sudoku(seed=randrange(sys.maxsize)).board
        self.board: Board = copy_board(self.puzzle)
        self.steps: list[Step] = []

    def backtrack_solve(self) -> bool:
        pos = self._find_next_empty_pos(self.board)
        if pos is None:
            return True
        y, x = pos
        for digit in range(1, 10):
            if not self._check_new_digit_valid(y, x, digit):
                continue
            self.board[y][x] = digit
            step: Step = (y, x, digit)
            self.steps.append(step)
            if self.backtrack_solve():
                return True
            self.steps.pop()
            self.board[y][x] = None
        return False

    def _find_next_empty_pos(self, board: Board) -> tuple[int, int] | None:
        for y in range(9):
            for x in range(9):
                if board[y][x] is not None:
                    continue
                return (y, x)
        return None

    def _check_new_digit_valid(self, y: int, x: int, digit: int) -> bool:
        if self.board[y].count(digit):
            return False
        if transpose(self.board)[x].count(digit):
            return False
        if get_square(self.board, y, x).count(digit):
            return False
        return True
