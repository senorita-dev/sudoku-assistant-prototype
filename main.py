from dash import Dash, Input, Output, State, ctx, dcc, html, no_update
import components
import methods
import type_defs

app = Dash(__name__)


app.layout = html.Div(
    [
        dcc.Store(id="sudoku-data", storage_type="memory"),
        html.H1("Sudoku"),
        html.Div(id="sudoku-div"),
        html.Div(
            [
                html.Button("New", id="new-btn"),
                html.Button("⏮", id="jump-to-start-btn"),
                html.Button("◀", id="previous-btn"),
                html.Button("▶", id="next-btn"),
                html.Button("⏭", id="jump-to-end-btn"),
            ]
        ),
        html.Div(id="sudoku-step"),
    ],
    style={"display": "inline-block"},
)


@app.callback(
    Output("sudoku-step", "children"),
    Input("sudoku-data", "data"),
    prevent_initial_call=True,
)
def render_sudoku_step(data: type_defs.SudokuData | None):
    if data is None:
        return no_update

    if data["step_index"] == -1:
        return [html.H3(f"Step 0 of {len(data["steps"])}")]

    step = data["steps"][data["step_index"]]
    (y, x, digit) = step
    return [
        html.H3(f"Step {data["step_index"] + 1} of {len(data["steps"])}"),
        html.P(f"Place digit {digit} at row {y+1} column {x+1} because [reason]."),
    ]


@app.callback(
    Output("sudoku-div", "children"),
    Input("sudoku-data", "data"),
)
def render_sudoku_board(data: type_defs.SudokuData | None):
    if data is None:
        return components.sudoku_table(methods.empty_board())
    return components.sudoku_table(data["board"])


@app.callback(
    Output("jump-to-start-btn", "disabled"),
    Output("previous-btn", "disabled"),
    Output("next-btn", "disabled"),
    Output("jump-to-end-btn", "disabled"),
    Input("sudoku-data", "data"),
    prevent_initial_call=True,
)
def toggle_solution_step_buttons(data: type_defs.SudokuData | None):
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
    State("sudoku-data", "data"),
    Input("new-btn", "n_clicks"),
    Input("jump-to-start-btn", "n_clicks"),
    Input("previous-btn", "n_clicks"),
    Input("next-btn", "n_clicks"),
    Input("jump-to-end-btn", "n_clicks"),
    prevent_initial_call=True,
)
def update_sudoku_data(
    data: type_defs.SudokuData,
    new_btn_n_clicks,
    jump_to_start_btn_n_clicks,
    previous_btn_n_clicks,
    next_btn_n_clicks,
    jump_to_end_btn_n_clicks,
):
    if ctx.triggered_id == "new-btn":
        sudoku = methods.SudokuManager()
        sudoku.backtrack_solve()
        return {"board": sudoku.board, "steps": sudoku.steps, "step_index": -1}

    board = data["board"]
    steps = data["steps"]
    index = data["step_index"]

    if ctx.triggered_id == "jump-to-start-btn":
        if index == -1:
            return no_update
        for curr_step_index in range(index - 1, -1, -1):
            y, x, _ = steps[curr_step_index]
            board[y][x] = None
        data["step_index"] = -1
        return data

    if ctx.triggered_id == "previous-btn":
        if index == -1:
            return no_update
        data["step_index"] -= 1
        y, x, _ = steps[data["step_index"]]
        board[y][x] = None
        return data

    if ctx.triggered_id == "next-btn":
        if index == len(steps) - 1:
            return no_update
        y, x, digit = steps[data["step_index"]]
        board[y][x] = digit
        data["step_index"] += 1
        return data

    if ctx.triggered_id == "jump-to-end-btn":
        if index == len(steps) - 1:
            return no_update
        for curr_step_index in range(index, len(steps)):
            y, x, digit = steps[curr_step_index]
            board[y][x] = digit
        data["step_index"] = curr_step_index
        return data

    return no_update


if __name__ == "__main__":
    app.run(debug=True)
