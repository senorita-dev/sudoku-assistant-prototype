from typing import TypedDict


Board = list[list[int | None]]
CandidatesBoard = list[list[list[int] | int | None]]
Step = tuple[int, int, int, list[tuple[int, int]]]


class SudokuData(TypedDict):
    board: CandidatesBoard
    puzzle: Board
    steps: list[Step]
    step_index: int
