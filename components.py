from dash import html
import type_defs


def sudoku_table(board: type_defs.ReductionBoard) -> html.Table:
    return html.Table(
        [
            html.Tbody(
                [
                    html.Tr([sudoku_cell(board, y, x) for x in range(9)])
                    for y in range(9)
                ]
            )
        ],
        style={
            "border": "3px solid black",
            "borderCollapse": "collapse",
            "margin": "0 auto",
        },
    )


def sudoku_cell(board: type_defs.ReductionBoard, y: int, x: int):
    cell = board[y][x]
    return html.Td(
        (
            ""
            if cell is None
            else candidates_cell(cell) if isinstance(cell, list) else cell
        ),
        style={
            "width": "40px",
            "height": "40px",
            "textAlign": "center",
            "border": "1px solid black",
            "fontSize": "24px",
            "borderTop": ("3px solid black" if y % 3 == 0 else ""),
            "borderLeft": ("3px solid black" if x % 3 == 0 else ""),
        },
    )


def candidates_cell(digits: list[int]):
    return html.Div(
        [
            html.Span(
                digit if digit in digits else "",
                style={
                    "display": "flex",
                    "justify-content": "center",
                    "align-items": "center",
                    "overflow": "hidden",
                },
            )
            for digit in range(1, 10)
        ],
        style={
            "display": "grid",
            "gridTemplateRows": "repeat(3, 1fr)",
            "gridTemplateColumns": "repeat(3, 1fr)",
            "width": "inherit",
            "height": "inherit",
            "overflow": "hidden",
            "fontSize": "10px",
        },
    )
