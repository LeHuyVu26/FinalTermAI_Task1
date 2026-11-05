from typing import List, Sequence
from .min_conflicts import MaxConflictMinConflictsSolver, MinConflictsSolver
from .sat_solver import SATQueensSolver

def print_table(headers: Sequence[str], rows: List[Sequence]):
    widths = [max(len(str(x)) for x in col) for col in zip(headers, *rows)]
    line = " | ".join(str(h).ljust(w) for h, w in zip(headers, widths))
    print(line)
    print("-+-".join("-" * w for w in widths))
    for row in rows:
        print(" | ".join(str(x).ljust(w) for x, w in zip(row, widths)))

class Benchmark:
    def run_sat(self, sizes: Sequence[int]):
        rows = []
        for n in sizes:
            res = SATQueensSolver().solve(n)
            rows.append((n, res.num_vars, res.num_clauses, f"{res.encode_time_s:.4f}",
                         f"{res.time_s:.4f}", res.solved))
        print_table(["N", "#vars", "#clauses", "encode(s)", "solve(s)", "valid"], rows)

    def run_min_conflicts(self, sizes: Sequence[int], runs: int = 20, seed: int = 0):
        rows = []
        for n in sizes:
            for factory in (lambda s: MinConflictsSolver(seed=s),
                            lambda s: MaxConflictMinConflictsSolver(seed=s)):
                results = [factory(seed + i).solve(n) for i in range(runs)]
                ok = [r for r in results if r.solved]
                avg = lambda xs: sum(xs) / len(xs) if xs else float("nan")
                rows.append((n, results[0].solver, f"{len(ok)}/{runs}",
                             f"{avg([r.steps for r in ok]):.1f}",
                             f"{avg([r.time_s for r in ok]):.4f}"))
        print_table(["N", "algorithm", "success", "avg steps", "avg time(s)"], rows)