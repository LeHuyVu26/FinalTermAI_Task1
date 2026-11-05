import random
from time import perf_counter
from typing import List, Optional
from .models import Board, QueensSolver, SolveResult

class QueenState:
    def __init__(self, n: int, rng: random.Random):
        self.n = n
        self.rows = [rng.randrange(n) for _ in range(n)]
        self.row_cnt = [0] * n
        self.d1 = [0] * (2 * n - 1)   # r - c + n - 1
        self.d2 = [0] * (2 * n - 1)   # r + c
        for c, r in enumerate(self.rows):
            self._add(c, r, 1)

    def _add(self, c: int, r: int, delta: int):
        self.row_cnt[r] += delta
        self.d1[r - c + self.n - 1] += delta
        self.d2[r + c] += delta

    def conflicts(self, c: int) -> int:
        r = self.rows[c]
        return (self.row_cnt[r] - 1) + (self.d1[r - c + self.n - 1] - 1) + (self.d2[r + c] - 1)

    def conflicted_columns(self) -> List[int]:
        return [c for c in range(self.n) if self.conflicts(c) > 0]

    def best_rows(self, c: int) -> List[int]:
        r0 = self.rows[c]
        self._add(c, r0, -1)
        n = self.n
        costs = [self.row_cnt[r] + self.d1[r - c + n - 1] + self.d2[r + c] for r in range(n)]
        self._add(c, r0, 1)
        m = min(costs)
        best = [r for r in range(n) if costs[r] == m]
        if len(best) > 1 and r0 in best:
            best.remove(r0)
        return best

    def move(self, c: int, r: int):
        self._add(c, self.rows[c], -1)
        self.rows[c] = r
        self._add(c, r, 1)


class MinConflictsSolver(QueensSolver):
    
    name = "Min-Conflicts"

    def __init__(self, max_steps: Optional[int] = None, seed: Optional[int] = None):
        self.max_steps = max_steps
        self.rng = random.Random(seed)

    def select_variable(self, state: QueenState, conflicted: List[int]) -> int:
        return self.rng.choice(conflicted)

    def solve(self, n: int) -> SolveResult:
        max_steps = self.max_steps or max(10_000, 50 * n)
        t0 = perf_counter()
        state = QueenState(n, self.rng)
        steps, solved = 0, False
        while steps <= max_steps:
            conflicted = state.conflicted_columns()
            if not conflicted:
                solved = True
                break
            c = self.select_variable(state, conflicted)
            state.move(c, self.rng.choice(state.best_rows(c)))
            steps += 1
        elapsed = perf_counter() - t0
        return SolveResult(n, self.name, solved, list(state.rows), elapsed, steps)


class MaxConflictMinConflictsSolver(MinConflictsSolver):

    name = "Min-Conflicts + MaxConflict"

    def __init__(self, max_steps: Optional[int] = None, seed: Optional[int] = None, noise: float = 0.1):
        super().__init__(max_steps, seed)
        self.noise = noise

    def select_variable(self, state: QueenState, conflicted: List[int]) -> int:
        if self.rng.random() < self.noise:
            return self.rng.choice(conflicted)
        counts = [(state.conflicts(c), c) for c in conflicted]
        top = max(k for k, _ in counts)
        return self.rng.choice([c for k, c in counts if k == top])