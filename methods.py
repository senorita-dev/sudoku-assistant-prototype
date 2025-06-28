from sudoku import Sudoku, sys
from random import randrange
import sys
from type_defs import Board, Step


def empty_board() -> Board:
    return [[None for _ in range(9)] for _ in range(9)]


def copy_board(board: Board) -> Board:
    return [row.copy() for row in board]


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

    def logic_solve(self) -> bool:
        if not self._candidates_board():
            return False
        solving_methods = [self._naked_single]
        progress_made = True
        while progress_made:
            progress_made = False
            for method in solving_methods:
                if not method():
                    continue
                progress_made = True
                break
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
        if self._get_transpose()[x].count(digit):
            return False
        if self._get_square(y, x).count(digit):
            return False
        return True

    def _get_transpose(self) -> Board:
        new_board = empty_board()
        for y in range(9):
            for x in range(9):
                new_board[y][x] = self.board[x][y]
        return new_board

    def _get_square(self, y: int, x: int) -> list[int | None]:
        min_y = (y // 3) * 3
        max_y = (y // 3) * 3 + 3
        min_x = (x // 3) * 3
        max_x = (x // 3) * 3 + 3
        return [
            self.board[curr_y][curr_x]
            for curr_x in range(min_x, max_x)
            for curr_y in range(min_y, max_y)
        ]

    def _candidates_board(self) -> bool:
        solvable = True
        for y in range(9):
            for x in range(9):
                if self.board[y][x] is not None:
                    continue
                digits = [
                    digit
                    for digit in range(1, 10)
                    if self._check_new_digit_valid(y, x, digit)
                ]
                if len(digits) == 0:
                    solvable = False
                self.board[y][x] = digits
        self.puzzle = copy_board(self.board)
        return solvable

    def _update_candidates_for_new_cell(self, y: int, x: int):
        digit = self.board[y][x]
        for cells in (self.board[y], self._get_transpose()[x], self._get_square(y, x)):
            for cell in cells:
                if not isinstance(cell, list) or digit not in cell:
                    continue
                cell.remove(digit)
        return

    def _naked_single(self) -> bool:
        progress_made = False
        for y in range(9):
            for x in range(9):
                cell = self.board[y][x]
                if not isinstance(cell, list) or len(cell) != 1:
                    continue
                digit = cell[0]
                step: Step = (y, x, digit)
                self.steps.append(step)
                self.board[y][x] = digit
                self._update_candidates_for_new_cell(y, x)
                progress_made = True
        return progress_made
