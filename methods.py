from sudoku import Sudoku
from random import randrange
import sys
from type_defs import Board, CandidatesBoard, Step
from copy import deepcopy


def empty_board() -> Board:
    return [[None for _ in range(9)] for _ in range(9)]


def copy_board(board: CandidatesBoard) -> CandidatesBoard:
    return deepcopy(board)


class SudokuManager:
    def __init__(self):
        self.puzzle: Board = Sudoku(seed=randrange(sys.maxsize)).board
        self.board: Board = copy_board(self.puzzle)
        self.steps: list[Step] = []

    def logic_solve(self) -> bool:
        if not self._candidates_board():
            return False
        solving_methods = [self._naked_single, self._hidden_single]
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
        return [
            self.board[curr_y][curr_x]
            for (curr_y, curr_x) in self._get_square_coords(y, x)
        ]

    def _get_square_coords(self, y: int, x: int) -> list[tuple[int, int]]:
        min_y = (y // 3) * 3
        max_y = (y // 3) * 3 + 3
        min_x = (x // 3) * 3
        max_x = (x // 3) * 3 + 3
        return [
            (curr_y, curr_x)
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

    def _update_candidates_for_new_cell(self, y: int, x: int) -> list[tuple[int, int]]:
        removed_candidates = []
        digit = self.board[y][x]
        for curr_x, cell in enumerate(self.board[y]):
            if not isinstance(cell, list) or digit not in cell:
                continue
            cell.remove(digit)
            removed_candidates.append((y, curr_x))
        for curr_y, cell in enumerate(self._get_transpose()[x]):
            if not isinstance(cell, list) or digit not in cell:
                continue
            cell.remove(digit)
            removed_candidates.append((curr_y, x))
        for curr_y, curr_x in self._get_square_coords(y, x):
            cell = self.board[curr_y][curr_x]
            if not isinstance(cell, list) or digit not in cell:
                continue
            cell.remove(digit)
            removed_candidates.append((curr_y, curr_x))
        return removed_candidates

    def _naked_single(self) -> bool:
        progress_made = False
        for y in range(9):
            for x in range(9):
                cell = self.board[y][x]
                if not isinstance(cell, list) or len(cell) != 1:
                    continue
                digit = cell[0]
                self.board[y][x] = digit
                step: Step = {
                    "type": "fill",
                    "name": "Naked Single",
                    "digit": digit,
                    "position": (y, x),
                    "candidates_removed_positions": self._update_candidates_for_new_cell(
                        y, x
                    ),
                }
                self.steps.append(step)
                progress_made = True
        return progress_made

    def _hidden_single(self) -> bool:
        rows_digit_map = [{digit: [] for digit in range(1, 10)} for _ in range(9)]
        cols_digit_map = [{digit: [] for digit in range(1, 10)} for _ in range(9)]
        squares_digit_map = [{digit: [] for digit in range(1, 10)} for _ in range(9)]
        for y in range(9):
            for x in range(9):
                cell = self.board[y][x]
                if not isinstance(cell, list):
                    continue
                for digit in cell:
                    rows_digit_map[y][digit].append((y, x))
                    cols_digit_map[x][digit].append((y, x))
                    square_index = (y // 3) * 3 + (x // 3)
                    squares_digit_map[square_index][digit].append((y, x))
        for digits_map in (rows_digit_map, cols_digit_map, squares_digit_map):
            for digit_map in digits_map:
                for digit, positions in digit_map.items():
                    if len(positions) != 1:
                        continue
                    y, x = positions[0]
                    self.board[y][x] = digit
                    step: Step = {
                        "type": "fill",
                        "name": "Hidden Single",
                        "digit": digit,
                        "position": (y, x),
                        "candidates_removed_positions": self._update_candidates_for_new_cell(
                            y, x
                        ),
                    }
                    self.steps.append(step)
                    return True
        return False
