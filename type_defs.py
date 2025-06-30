from typing import TypedDict, Literal


Board = list[list[int | None]]
CandidatesBoard = list[list[list[int] | int | None]]


class FillStep(TypedDict):
    type: Literal["fill"]
    position: tuple[int, int]
    digit: int
    candidates_removed_positions: list[tuple[int, int]]


class ReduceStep(TypedDict):
    type: Literal["reduce"]
    positions: list[tuple[int, int]]
    digits: list[int]
    candidates_removed_positions: list[tuple[int, int]]


Step = FillStep | ReduceStep


class SudokuData(TypedDict):
    board: CandidatesBoard
    puzzle: Board
    steps: list[Step]
    step_index: int
