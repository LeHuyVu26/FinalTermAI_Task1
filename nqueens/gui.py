import tkinter as tk
from tkinter import ttk, messagebox
from .min_conflicts import MaxConflictMinConflictsSolver, MinConflictsSolver
from .models import Board

class QueensApp(tk.Tk):
    SIZE = 640

    def __init__(self):
        super().__init__()
        self.title("N-Queens Solver")
        self.algos = {
            "SAT (Glucose3)": None,
            "Min-Conflicts": MinConflictsSolver,
            "Min-Conflicts + MaxConflict": MaxConflictMinConflictsSolver,
        }
        bar = ttk.Frame(self)
        bar.pack(fill="x", padx=8, pady=6)
        ttk.Label(bar, text="N:").pack(side="left")
        self.n_var = tk.IntVar(value=8)
        ttk.Spinbox(bar, from_=4, to=200, textvariable=self.n_var, width=5).pack(side="left", padx=4)
        self.algo_var = tk.StringVar(value="SAT (Glucose3)")
        ttk.Combobox(bar, textvariable=self.algo_var, values=list(self.algos),
                     state="readonly", width=28).pack(side="left", padx=4)
        ttk.Button(bar, text="Solve", command=self.on_solve).pack(side="left", padx=4)
        self.status = tk.StringVar(value="Chọn N và thuật toán rồi bấm Solve.")
        ttk.Label(self, textvariable=self.status).pack(fill="x", padx=8)
        self.canvas = tk.Canvas(self, width=self.SIZE, height=self.SIZE, bg="white")
        self.canvas.pack(padx=8, pady=8)
        self.draw(None, self.n_var.get())

    def make_solver(self):
        name = self.algo_var.get()
        if name.startswith("SAT"):
            from .sat_solver import SATQueensSolver
            return SATQueensSolver()
        return self.algos[name]()

    def on_solve(self):
        try:
            n = int(self.n_var.get())
            result = self.make_solver().solve(n)
        except Exception as exc:
            messagebox.showerror("Lỗi", str(exc))
            return
        self.draw(result.queens, n)
        extra = (f"clauses={result.num_clauses}" if result.num_clauses else f"steps={result.steps}")
        self.status.set(f"{result.solver} | N={n} | solved={result.solved} | "
                        f"time={result.time_s:.4f}s | {extra}")

    def draw(self, queens, n):
        self.canvas.delete("all")
        cell = self.SIZE / n
        for r in range(n):
            for c in range(n):
                color = "#f0d9b5" if (r + c) % 2 == 0 else "#b58863"
                self.canvas.create_rectangle(c * cell, r * cell, (c + 1) * cell, (r + 1) * cell,
                                             fill=color, outline="")
        if not queens:
            return
        valid = Board.is_valid(queens)
        for c, r in enumerate(queens):
            x, y = (c + .5) * cell, (r + .5) * cell
            if cell >= 24:
                self.canvas.create_text(x, y, text="♛", font=("Arial", int(cell * .7)),
                                        fill="#1b5e20" if valid else "red")
            else:
                rad = cell * .4
                self.canvas.create_oval(x - rad, y - rad, x + rad, y + rad,
                                        fill="#1b5e20" if valid else "red", outline="")

def launch():
    QueensApp().mainloop()