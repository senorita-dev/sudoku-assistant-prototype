from dash import html
import type_defs
import methods


def sudoku_table(data: type_defs.SudokuData | None) -> html.Table:
    return html.Table(
        [
            html.Tbody(
                [html.Tr([sudoku_cell(data, y, x) for x in range(9)]) for y in range(9)]
            )
        ],
        style={
            "border": "3px solid black",
            "borderCollapse": "collapse",
            "margin": "0 auto",
        },
    )


def sudoku_cell(data: type_defs.SudokuData | None, y: int, x: int):
    board = methods.empty_board() if data is None else data["board"]
    step = (
        None
        if data is None or data["step_index"] <= -1
        else data["steps"][data["step_index"]]
    )
    [new_y, new_x] = [None, None] if step is None else step["position"]
    cell = board[y][x]
    return html.Td(
        (
            ""
            if cell is None
            else (candidates_cell(y, x, cell, step) if isinstance(cell, list) else cell)
        ),
        style={
            "width": "40px",
            "height": "40px",
            "textAlign": "center",
            "border": "1px solid black",
            "fontSize": "24px",
            "borderTop": ("3px solid black" if y % 3 == 0 else ""),
            "borderLeft": ("3px solid black" if x % 3 == 0 else ""),
            "backgroundColor": ("lightgreen" if y == new_y and x == new_x else None),
        },
    )


def candidates_cell(y: int, x: int, digits: list[int], step: type_defs.Step | None):
    if step is None:
        new_digit = None
    elif step["type"] == "fill":
        new_digit = step["digit"]
        positions = step["candidates_removed_positions"]
    elif step["type"] == "reduce":
        return "TO-DO"
    return html.Div(
        [
            html.Span(
                digit if digit in digits else "",
                style={
                    "display": "flex",
                    "justifyContent": "center",
                    "alignItems": "center",
                    "overflow": "hidden",
                    "padding": "4px",
                    "borderRadius": "32px",
                    "backgroundColor": (
                        "red" if digit == new_digit and [y, x] in positions else None
                    ),
                    "color": (
                        "white" if digit == new_digit and [y, x] in positions else None
                    ),
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
