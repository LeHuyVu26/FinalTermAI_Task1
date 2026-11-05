# Task 1: N-Queens Solver
### Propositional Logic (SAT Solver) & Local Search (Min-Conflicts)

An Object-Oriented Python implementation of the **N-Queens Problem**, featuring two solving approaches:

- **Propositional Logic (SAT Solver):** Models the N-Queens problem using logical constraints and solves it with PySAT (Glucose3).
- **Local Search (Min-Conflicts):** Implements Standard and Heuristic Min-Conflicts algorithms to find valid solutions efficiently.

The project also includes a **Tkinter GUI** for interactive board visualization and experimental benchmarks for performance evaluation.

---

## Project Structure

```text
AI_Task1/
│
├── nqueens/
│   ├── __init__.py
│   ├── models.py           # Data models (Board, SolveResult, base class)
│   ├── constraints.py      # Constraint discovery and CNF conversion
│   ├── sat_solver.py       # SAT Solver using PySAT (Glucose3)
│   ├── min_conflicts.py    # Local Search (Standard & Heuristic variants)
│   ├── benchmark.py        # Experimental evaluation script
│   └── gui.py              # Tkinter GUI for board visualization
│
├── main.py                 # Entry point (CLI commands & GUI launcher)
├── task1_nqueens.ipynb     # Jupyter Notebook with experimental results
├── requirements.txt        # Project dependencies
└── README.md               # Project documentation
```

---

## Installation & Setup

### 1. Create a Virtual Environment

Python **3.11** is recommended.

**Windows (PowerShell):**

```powershell
py -3.11 -m venv venv
.\venv\Scripts\Activate.ps1
```

**macOS / Linux:**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Install Dependencies

```bash
python -m pip install -r requirements.txt
```

---

## Running the Application

### 1. Interactive GUI

Launch the Tkinter graphical interface to visualize the N-Queens board and observe the solving process.

```bash
python main.py gui
```

### 2. Experimental Benchmarks

Run the following commands to evaluate the performance of the implemented algorithms

## Launch GUI
python main.py gui

## Solve using SAT Solver (N = 8)
python main.py sat -n 8

## Solve using Standard Min-Conflicts (N = 50)
python main.py mc -n 50 --seed 1

## Solve using Heuristic Min-Conflicts (N = 50)
python main.py mc-heuristic -n 50 --seed 1

## Benchmark SAT Solver (default sizes)
python main.py bench-sat

## Benchmark SAT Solver (N = 4, 8, 16, 32)
python main.py bench-sat --sizes 4 8 16 32

## Benchmark Min-Conflicts (20 runs)
python main.py bench-mc --runs 20

---

## Experimental Results

Experimental outputs and performance evaluations are documented in:

- `task1_nqueens.ipynb` – Jupyter Notebook containing the experimental results and analysis.

---

## Technologies Used

- **Python 3.11**
- **PySAT** – SAT solving with Glucose3
- **Tkinter** – Graphical User Interface
- **Jupyter Notebook** – Experimental evaluation

---

**Developed for AI Task 1 – N-Queens Problem.**
