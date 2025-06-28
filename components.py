from dash import html


def sudoku_table(board) -> html.Table:
    return html.Table(
        [
            html.Tbody(
                [
                    html.Tr(
                        [
                            html.Td(
                                "" if board[y][x] is None else board[y][x],
                                style={
                                    "width": "40px",
                                    "height": "40px",
                                    "textAlign": "center",
                                    "border": "1px solid black",
                                    "fontSize": "20px",
                                    "borderTop": (
                                        "3px solid black" if y % 3 == 0 else ""
                                    ),
                                    "borderLeft": (
                                        "3px solid black" if x % 3 == 0 else ""
                                    ),
                                },
                            )
                            for x in range(9)
                        ]
                    )
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
