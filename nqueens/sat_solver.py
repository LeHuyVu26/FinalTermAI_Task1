from time import perf_counter
from pysat.solvers import Glucose3
from .constraints import CNFConverter, ConstraintDiscoverer
from .models import Board, QueensSolver, SolveResult

class SATQueensSolver(QueensSolver):
    name = "SAT (Glucose3)"

    def solve(self, n: int) -> SolveResult:
        board = Board(n)

        t0 = perf_counter()
        constraints = ConstraintDiscoverer(board).discover()
        clauses = CNFConverter(board).convert(constraints)
        encode_time = perf_counter() - t0

        t1 = perf_counter()
        queens = None
        with Glucose3(bootstrap_with=clauses) as solver:
            sat = solver.solve()
            model = solver.get_model() if sat else None
        solve_time = perf_counter() - t1

        if model:
            queens = [-1] * n
            for lit in model:
                if lit > 0:
                    r, c = board.cell(lit)
                    queens[c] = r
        solved = Board.is_valid(queens)
        return SolveResult(n, self.name, solved, queens, solve_time, 0,
                           board.num_vars, len(clauses), encode_time)