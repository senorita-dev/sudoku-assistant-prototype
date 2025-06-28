from typing import TypedDict


Board = list[list[int | None]]
ReductionBoard = list[list[list[int] | int | None]]
Step = tuple[int, int, int]


class SudokuData(TypedDict):
    board: Board
    steps: list[Step]
    step_index: int
