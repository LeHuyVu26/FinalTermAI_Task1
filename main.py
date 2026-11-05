"""Entry point: python main.py {gui|sat|mc|bench-sat|bench-mc} ..."""
import argparse

from nqueens.models import Board


def show(result):
    print(f"[{result.solver}] N={result.n} solved={result.solved} time={result.time_s:.4f}s "
          f"steps={result.steps} vars={result.num_vars} clauses={result.num_clauses}")
    if result.queens and result.n <= 20:
        print(Board.to_text(result.queens))


def main():
    p = argparse.ArgumentParser(description="N-Queens: SAT & Min-Conflicts")
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("gui", help="mở giao diện")
    for name in ("sat", "mc", "mc-heuristic"):
        s = sub.add_parser(name)
        s.add_argument("-n", type=int, default=8)
        s.add_argument("--seed", type=int, default=None)
    b1 = sub.add_parser("bench-sat")
    b1.add_argument("--sizes", type=int, nargs="+", default=[4, 8, 12, 16, 20, 24, 32, 40, 48, 64])
    b2 = sub.add_parser("bench-mc")
    b2.add_argument("--sizes", type=int, nargs="+", default=[8, 16, 32, 64, 100, 200, 500, 1000])
    b2.add_argument("--runs", type=int, default=20)
    b2.add_argument("--seed", type=int, default=0)
    a = p.parse_args()

    if a.cmd == "gui":
        from nqueens.gui import launch
        launch()
    elif a.cmd == "sat":
        from nqueens.sat_solver import SATQueensSolver
        show(SATQueensSolver().solve(a.n))
    elif a.cmd == "mc":
        from nqueens.min_conflicts import MinConflictsSolver
        show(MinConflictsSolver(seed=a.seed).solve(a.n))
    elif a.cmd == "mc-heuristic":
        from nqueens.min_conflicts import MaxConflictMinConflictsSolver
        show(MaxConflictMinConflictsSolver(seed=a.seed).solve(a.n))
    elif a.cmd == "bench-sat":
        from nqueens.benchmark import Benchmark
        Benchmark().run_sat(a.sizes)
    elif a.cmd == "bench-mc":
        from nqueens.benchmark import Benchmark
        Benchmark().run_min_conflicts(a.sizes, a.runs, a.seed)


if __name__ == "__main__":
    main()
