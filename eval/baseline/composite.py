from __future__ import annotations
import time
from pathlib import Path

class CompositeBaseline:
    def __init__(self, root):
        self.root = Path(root)
    def trace_incident(self, endpoint):
        t0 = time.perf_counter()
        runs   = list((self.root/"mlflow").glob("*.json")) if (self.root/"mlflow").exists() else []
        atts   = list((self.root/"slsa").glob("*.json"))   if (self.root/"slsa").exists()   else []
        proofs = list((self.root/"rekor").glob("*.json"))  if (self.root/"rekor").exists()  else []
        return {"endpoint": endpoint, "runs_scanned": len(runs),
                "atts_scanned": len(atts), "proofs_scanned": len(proofs),
                "elapsed_ms": (time.perf_counter() - t0) * 1000}
