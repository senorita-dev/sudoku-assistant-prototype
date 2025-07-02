from dash import html
import type_defs


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
    style = {
        "width": "40px",
        "height": "40px",
        "textAlign": "center",
        "border": "1px solid black",
        "fontSize": "24px",
        "borderTop": ("3px solid black" if y % 3 == 0 else ""),
        "borderLeft": ("3px solid black" if x % 3 == 0 else ""),
    }
    if data is None:
        return html.Td("", style=style)
    board = data["board"]
    steps = data["steps"]
    step_index = data["step_index"]
    cell = board[y][x]
    if step_index <= -1:
        return html.Td(
            (
                ""
                if cell is None
                else (
                    candidates_cell(y, x, cell, None)
                    if isinstance(cell, list)
                    else cell
                )
            ),
            style=style,
        )
    step = steps[step_index]
    if step["type"] == "fill":
        [new_y, new_x] = step["position"]
        style = style | {
            "backgroundColor": "lightgreen" if y == new_y and x == new_x else None
        }
    else:
        positions = step["positions"]
        style = style | {
            "backgroundColor": "lightblue" if [y, x] in positions else None
        }
    return html.Td(
        (
            ""
            if cell is None
            else (candidates_cell(y, x, cell, step) if isinstance(cell, list) else cell)
        ),
        style=style,
    )


def candidates_cell(y: int, x: int, digits: list[int], step: type_defs.Step | None):
    divStyle = {
        "display": "grid",
        "gridTemplateRows": "repeat(3, 1fr)",
        "gridTemplateColumns": "repeat(3, 1fr)",
        "width": "inherit",
        "height": "inherit",
        "overflow": "hidden",
        "fontSize": "10px",
    }
    spanStyle = {
        "display": "flex",
        "justifyContent": "center",
        "alignItems": "center",
        "overflow": "hidden",
        "padding": "4px",
        "borderRadius": "32px",
    }
    if step is None:
        return html.Div(
            [
                html.Span(digit if digit in digits else "", style=spanStyle)
                for digit in range(1, 10)
            ],
            style=divStyle,
        )
    if step["type"] == "fill":
        new_digit = step["digit"]
        positions = step["candidates_removed_positions"]
        return html.Div(
            [
                html.Span(
                    digit if digit in digits else "",
                    style=spanStyle
                    | {
                        "backgroundColor": (
                            "red"
                            if digit == new_digit and [y, x] in positions
                            else None
                        ),
                        "color": (
                            "white"
                            if digit == new_digit and [y, x] in positions
                            else None
                        ),
                    },
                )
                for digit in range(1, 10)
            ],
            style=divStyle,
        )
    removed_digits = step["removed_digits"]
    positions = step["candidates_removed_positions"]
    return html.Div(
        [
            html.Span(
                digit if digit in digits else "",
                style=spanStyle
                | {
                    "backgroundColor": (
                        "red"
                        if digit in digits
                        and digit in removed_digits
                        and [y, x] in positions
                        else None
                    ),
                    "color": (
                        "white"
                        if digit in digits
                        and digit in removed_digits
                        and [y, x] in positions
                        else None
                    ),
                },
            )
            for digit in range(1, 10)
        ],
        style=divStyle,
    )
