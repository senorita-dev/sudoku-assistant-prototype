from dash import Dash, Input, Output, State, ctx, dcc, html, no_update
import dash_bootstrap_components as dbc
import components
import methods
import type_defs


app = Dash(
    __name__,
    title="Sudoku Assistant (prototype)",
    update_title="",
)

server = app.server

app.layout = html.Div(
    html.Div(
        [
            dcc.Store(id="sudoku-data", storage_type="memory"),
            html.H1(
                "Sudoku Assistant (prototype)",
                style={"fontSize": "1.5rem", "textAlign": "center"},
            ),
            html.P(
                "Sudoku Assistant prototype built with Python and Dash.",
                style={"textAlign": "center"},
            ),
            html.P(
                [
                    html.A(
                        "Github",
                        href="https://github.com/senorita-dev/sudoku-assistant-prototype",
                        target="_blank",
                        rel="noopener noreferrer",
                    ),
                    html.A(
                        "Website",
                        href="https://rensaito.com/",
                        target="_blank",
                        rel="noopener noreferrer",
                    ),
                ],
                style={"display": "flex", "justifyContent": "center", "gap": "1rem"},
            ),
            html.Div(id="sudoku-div"),
            html.Button("New", id="new-btn"),
            html.Div(
                [
                    html.Button("⏮", id="jump-to-start-btn"),
                    html.Button("◀", id="previous-btn"),
                    html.Button("▶", id="next-btn"),
                    html.Button("⏭", id="jump-to-end-btn"),
                    dbc.Checkbox(
                        id="view-board-details-toggle",
                        value=True,
                        persistence_type="local",
                        label="View board details",
                    ),
                    dcc.Slider(
                        id="step-index-slider",
                        min=None,
                        max=None,
                        step=1,
                        marks=None,
                        tooltip={"always_visible": True, "placement": "bottom"},
                    ),
                ],
                id="sudoku-solution-controls",
            ),
            html.Div(id="sudoku-step"),
        ],
        style={"maxWidth": "920px"},
    ),
    style={"display": "flex", "justifyContent": "center"},
)


@app.callback(
    Output("sudoku-step", "children"),
    Input("sudoku-data", "data"),
    prevent_initial_call=True,
)
def render_sudoku_step(data: type_defs.SudokuData | None):
    if data is None:
        return no_update

    if len(data["steps"]) == 0:
        return [
            html.H3("No logical next steps found."),
            html.P(
                "Try creating another Sudoku board or lowering the difficulty first."
            ),
        ]

    if data["step_index"] == -1:
        return [
            html.H3(f"Step 0 of {len(data["steps"])}"),
            html.B("Initial Candidate Elimination"),
            html.P("List all possible candidates for every unsolved cell."),
        ]

    step = data["steps"][data["step_index"]]
    if step["type"] == "fill":
        y, x = step["position"]
        digit = step["digit"]
        explanation = html.P(
            f"Place digit {digit} at row {y+1} column {x+1} because [reason]."
        )
    else:
        positions = [(y + 1, x + 1) for (y, x) in step["candidates_removed_positions"]]
        removed_digits = step["removed_digits"]
        explanation = html.P(
            f"Remove candidates {removed_digits} at positions {positions} because [reason]."
        )
    return [
        html.H3(f"Step {data["step_index"] + 1} of {len(data["steps"])}"),
        html.B(step["name"]),
        explanation,
    ]


@app.callback(
    Output("sudoku-div", "children"),
    Input("sudoku-data", "data"),
    Input("view-board-details-toggle", "value"),
)
def render_sudoku_board(data: type_defs.SudokuData | None, view_board_details: bool):
    return components.sudoku_table(
        apply_steps(data, view_board_details) if data is not None else None,
        view_board_details,
    )


@app.callback(
    Output("sudoku-solution-controls", "style"),
    State("sudoku-solution-controls", "style"),
    Input("sudoku-data", "data"),
)
def toggle_solution_controls_display(style, data: type_defs.SudokuData | None):
    if data is None or len(data["steps"]) == 0:
        return {"display": "none"}
    try:
        if style["display"] == "block":
            return no_update
    finally:
        return {"display": "block"}


@app.callback(
    Output("jump-to-start-btn", "disabled"),
    Output("previous-btn", "disabled"),
    Output("next-btn", "disabled"),
    Output("jump-to-end-btn", "disabled"),
    Input("sudoku-data", "data"),
)
def toggle_solution_controls_disabled(data: type_defs.SudokuData | None):
    if data is None:
        return [True, True, True, True]
    index = data["step_index"]
    if index <= -1:
        return [True, True, False, False]
    if index >= len(data["steps"]) - 1:
        return [False, False, True, True]
    return [False, False, False, False]


@app.callback(
    Output("sudoku-data", "data"),
    Output("step-index-slider", "min"),
    Output("step-index-slider", "max"),
    Output("step-index-slider", "value"),
    State("sudoku-data", "data"),
    Input("new-btn", "n_clicks"),
    Input("jump-to-start-btn", "n_clicks"),
    Input("previous-btn", "n_clicks"),
    Input("next-btn", "n_clicks"),
    Input("jump-to-end-btn", "n_clicks"),
    Input("step-index-slider", "value"),
    prevent_initial_call=True,
)
def update_sudoku_data(
    data: type_defs.SudokuData,
    new_btn_n_clicks,
    jump_to_start_btn_n_clicks,
    previous_btn_n_clicks,
    next_btn_n_clicks,
    jump_to_end_btn_n_clicks,
    step_index_slider_value,
):
    if ctx.triggered_id == "new-btn":
        sudoku = methods.SudokuManager()
        sudoku.logic_solve()
        return (
            {
                "puzzle": sudoku.puzzle,
                "board": sudoku.puzzle,
                "steps": sudoku.steps,
                "step_index": -1,
            },
            0,
            len(sudoku.steps),
            0,
        )

    steps = data["steps"]
    index = data["step_index"]
    match ctx.triggered_id:
        case "jump-to-start-btn":
            if index == -1:
                return no_update, no_update, no_update, no_update
            data["step_index"] = -1
        case "previous-btn":
            if index == -1:
                return no_update, no_update, no_update, no_update
            data["step_index"] -= 1
        case "next-btn":
            if index == len(steps) - 1:
                return no_update, no_update, no_update, no_update
            data["step_index"] += 1
        case "jump-to-end-btn":
            if index == len(steps) - 1:
                return no_update, no_update, no_update, no_update
            data["step_index"] = len(steps) - 1
        case "step-index-slider":
            if index == step_index_slider_value - 1:
                return no_update, no_update, no_update, no_update
            data["step_index"] = step_index_slider_value - 1
        case _:
            return no_update, no_update, no_update, no_update
    return data, no_update, no_update, data["step_index"] + 1


def apply_steps(
    data: type_defs.SudokuData, view_board_details: bool
) -> type_defs.SudokuData:
    steps = data["steps"]
    index = data["step_index"]
    if index < -1 or index > len(steps):
        data["step_index"] = -1
        return data
    board = methods.copy_board(data["puzzle"])
    for curr_step_index in range(index + 1):
        step = steps[curr_step_index]
        if step["type"] == "fill":
            y, x = step["position"]
            digit = step["digit"]
            board[y][x] = digit
            if curr_step_index == index and view_board_details:
                continue
            for [curr_y, curr_x] in step["candidates_removed_positions"]:
                board[curr_y][curr_x].remove(digit)
        else:
            removed_digits = step["removed_digits"]
            if curr_step_index == index and view_board_details:
                continue
            for digit in removed_digits:
                for [curr_y, curr_x] in step["candidates_removed_positions"]:
                    if digit not in board[curr_y][curr_x]:
                        continue
                    board[curr_y][curr_x].remove(digit)
    data["board"] = board
    data["step_index"] = index
    return data


if __name__ == "__main__":
    app.run(debug=True)
