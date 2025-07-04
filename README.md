# Sudoku Assistant (prototype)

A web-based Sudoku solving assistant that demonstrates step-by-step logical solving techniques. This interactive application generates Sudoku puzzles and walks through the solution process using human-like solving strategies.

## 🔗 Links

- **🚀 [Live Demo](https://rensaito.com/sudoku-assistant-prototype)** - Try the application in your browser
- **✨ [Full Version](https://github.com/senorita-dev/sudoku-assistant)** - Full version with additional features _(coming soon)_

> **Note**: This is a prototype version. For the latest features and improvements, check out the full version linked above.

## Features

- **Puzzle Generation**: Automatically generates valid Sudoku puzzles with unique solutions
- **Step-by-Step Solving**: Demonstrates logical solving techniques used by human solvers
- **Interactive Visualization**: Visual representation of candidates and solving steps
- **Multiple Solving Techniques**:
  - Naked Single
  - Hidden Single
  - Naked Pair/Triple
  - Pointing Pair/Triple
  - Claiming Pair/Triple
- **Navigation Controls**: Step through the solution process at your own pace
- **Board Details Toggle**: Show/hide candidate numbers and step highlights

## Screenshots

The application displays a 9x9 Sudoku grid with:

- Green highlighting for newly placed numbers
- Red highlighting for eliminated candidates
- Blue highlighting for key candidates in elimination steps
- Small candidate numbers in empty cells

## Installation

### Prerequisites

- Python 3.13
- pip package manager

### Setup

1. Clone the repository:

```bash
git clone https://github.com/senorita-dev/sudoku-assistant-prototype
cd sudoku-assistant-prototype
```

2. Create a virtual environment (recommended):

```bash
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

1. Start the application:

```bash
python main.py
```

2. Open your web browser and navigate to `http://localhost:8050`

3. Use the interface:
   - Click **"New"** to generate a fresh Sudoku puzzle
   - Use navigation buttons to step through the solution:
     - ⏮ Jump to start
     - ◀ Previous step
     - ▶ Next step
     - ⏭ Jump to end
   - Toggle **"View board details"** to show/hide candidate highlighting
   - Use the slider to jump to any specific step

## Technical Details

### Architecture

The application is built using:

- **Dash**: Web application framework for Python
- **Dash Bootstrap Components**: UI components and styling
- **py-sudoku**: Sudoku puzzle generation library

### Project Structure

```
sudoku-python/
├── main.py           # Main application entry point and callbacks
├── methods.py        # Core Sudoku solving logic and algorithms
├── components.py     # UI components for the Sudoku board
├── type_defs.py      # TypeScript-style type definitions
├── requirements.txt  # Python dependencies
└── README.md         # This file
```

### Solving Algorithms

The application implements several logical solving techniques:

1. **Naked Single**: When a cell has only one possible candidate
2. **Hidden Single**: When a digit can only go in one cell within a row, column, or box
3. **Naked Pair**: When two cells in a unit contain the same two candidates
4. **Naked Triple**: When three cells in a unit contain the same three candidates
5. **Pointing Pair/Triple**: When candidates in a box point to a single row/column
6. **Claiming Pair/Triple**: When candidates in a row/column are confined to a single box

### Data Types

- `Board`: 9x9 grid of integers or None
- `CandidatesBoard`: Board that can also contain lists of candidate numbers
- `Step`: Union type for fill steps and candidate reduction steps
- `SudokuData`: Complete state including board, steps, and current position

## Development

### Adding New Solving Techniques

To add a new solving method:

1. Implement the method in `SudokuManager` class in `methods.py`
2. Add it to the `solving_methods` list in the `logic_solve()` method
3. Ensure it returns `True` if progress was made, `False` otherwise
4. Create appropriate `Step` objects to track the solving process

### Customizing the UI

The visual appearance can be modified in `components.py`:

- Adjust cell styling in `sudoku_cell()`
- Modify candidate display in `candidates_cell()`
- Update colors and highlighting logic

## Dependencies

- `py-sudoku==2.0.0`: Sudoku puzzle generation
- `dash==3.1.0`: Web application framework
- `dash-bootstrap-components==2.0.3`: Bootstrap UI components

## License

This project is a prototype for educational purposes.

## Author

Created by [Ren Saito](https://rensaito.com/)

- GitHub: [@senorita-dev](https://github.com/senorita-dev)

## Future Enhancements

Potential improvements for future versions:

- More advanced solving techniques (X-Wing, Swordfish, etc.)
- Difficulty level selection
- Puzzle input from user
- Solution validation
- Performance metrics and statistics
- Mobile-responsive design
- Export/import functionality
