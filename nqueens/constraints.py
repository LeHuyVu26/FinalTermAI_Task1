from dataclasses import dataclass
from itertools import combinations
from typing import Iterator, List, Tuple
from .models import Board

Cell = Tuple[int, int]

@dataclass(frozen=True)
class Constraint:
    kind: str
    source: str
    cells: Tuple[Cell, ...]

class ConstraintDiscoverer:

    def __init__(self, board: Board):
        self.board = board

    def _group(self, key_fn) -> List[Tuple[Cell, ...]]:
        groups = {}
        n = self.board.n
        for r in range(n):
            for c in range(n):
                groups.setdefault(key_fn(r, c), []).append((r, c))
        return [tuple(v) for v in groups.values()]

    def discover(self) -> List[Constraint]:
        cons: List[Constraint] = []
        sources = {
            "row": lambda r, c: r,
            "col": lambda r, c: c,
            "diag": lambda r, c: r - c,
            "anti-diag": lambda r, c: r + c,
        }
        for name, fn in sources.items():
            for cells in self._group(fn):
                if name in ("row", "col"):
                    cons.append(Constraint("ALO", name, cells))
                if len(cells) >= 2:
                    cons.append(Constraint("AMO", name, cells))
        return cons

class CNFConverter:

    def __init__(self, board: Board):
        self.board = board

    def convert(self, constraints: List[Constraint]) -> List[List[int]]:
        return list(self.iter_clauses(constraints))

    def iter_clauses(self, constraints: List[Constraint]) -> Iterator[List[int]]:
        v = self.board.var
        for con in constraints:
            lits = [v(r, c) for r, c in con.cells]
            if con.kind == "ALO":
                yield lits
            else:
                for a, b in combinations(lits, 2):
                    yield [-a, -b]