from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List, Optional, Tuple

class Board:
    def __init__(self, n: int):
        if n < 1:
            raise ValueError("N phải >= 1")
        self.n = n

    def var(self, r: int, c: int) -> int:
        return r * self.n + c + 1

    def cell(self, var: int) -> Tuple[int, int]:
        return divmod(var - 1, self.n)

    @property
    def num_vars(self) -> int:
        return self.n * self.n

    @staticmethod
    def count_attacking_pairs(queens: List[int]) -> int:
        n, cnt = len(queens), 0
        for a in range(n):
            for b in range(a + 1, n):
                if queens[a] == queens[b] or abs(queens[a] - queens[b]) == b - a:
                    cnt += 1
        return cnt

    @classmethod
    def is_valid(cls, queens: Optional[List[int]]) -> bool:
        return queens is not None and cls.count_attacking_pairs(queens) == 0

    @staticmethod
    def to_text(queens: List[int]) -> str:
        n = len(queens)
        return "\n".join(" ".join("Q" if queens[c] == r else "." for c in range(n)) for r in range(n))

@dataclass
class SolveResult:
    n: int
    solver: str
    solved: bool
    queens: Optional[List[int]] = None  
    time_s: float = 0.0
    steps: int = 0
    num_vars: int = 0
    num_clauses: int = 0
    encode_time_s: float = 0.0
    info: dict = field(default_factory=dict)

class QueensSolver(ABC):
    name = "solver"

    @abstractmethod
    def solve(self, n: int) -> SolveResult:
        ...