from __future__ import annotations
from typing import Any, Dict
from ..supplyql.evaluator import BoundedPathEvaluator

class EnforcementGateway:
    def __init__(self, evaluator: BoundedPathEvaluator, mode: str = "blocking"):
        assert mode in ("blocking", "audit")
        self.evaluator = evaluator; self.mode = mode
    def _decide(self, ok):
        if ok: return "ALLOW"
        return "BLOCK" if self.mode == "blocking" else "FLAG"
    def deploy_gate(self, policy, ctx): return self._decide(self.evaluator.evaluate(policy, ctx))
    def load_gate(self, policy, ctx):   return self._decide(self.evaluator.evaluate(policy, ctx))
    def answer_gate(self, policy, ctx): return self._decide(self.evaluator.evaluate(policy, ctx))
    def proof_gate(self, policy, ctx):  return self._decide(self.evaluator.evaluate(policy, ctx))
