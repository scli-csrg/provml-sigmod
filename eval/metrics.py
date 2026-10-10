from dataclasses import dataclass

@dataclass
class RejectionMetrics:
    n_runs: int
    rejected: int
    false_rejected: int
    @property
    def rejection_rate(self): return self.rejected / max(1, self.n_runs)
    @property
    def false_rejection_rate(self): return self.false_rejected / max(1, self.n_runs)

def amdahl_overhead(base_ms, overhead_ms): return overhead_ms / max(base_ms, 1e-9)
