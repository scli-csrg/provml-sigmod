from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Dict, Optional
from ..query_store import QueryStore

@dataclass
class PathStep:
    node_type: str
    is_event: bool
    edge_label: Optional[str] = None

class BoundedPathEvaluator:
    def __init__(self, store: QueryStore, kmax: int = 6):
        self.store = store; self.kmax = kmax

    def evaluate(self, policy, context: Dict[str, Any]) -> bool:
        if policy is None:
            return bool(self.store.store._log)
        endpoint = context.get("endpoint") or context.get("answer_id")
        if endpoint is None: return False
        return self._eval_expr(policy.expr, endpoint, context)

    def _eval_expr(self, node, endpoint, ctx):
        if isinstance(node, tuple) and node[0] == "and_":
            return self._eval_expr(node[1], endpoint, ctx) and self._eval_expr(node[2], endpoint, ctx)
        if isinstance(node, tuple) and node[0] == "or_":
            return self._eval_expr(node[1], endpoint, ctx) or self._eval_expr(node[2], endpoint, ctx)
        if isinstance(node, tuple) and node[0] == "exists_path":
            return self._eval_exists(node, endpoint, ctx)
        if isinstance(node, tuple) and node[0] == "forall":
            return self._eval_forall(node, endpoint, ctx)
        return False

    def _eval_exists(self, node, endpoint, ctx):
        _, path, psi = node
        if len(path) > self.kmax: return False
        start = self._resolve_start(endpoint)
        if start is None: return False
        for ah in start:
            if self._walk(path, 0, ah, psi, ctx): return True
        return False

    def _walk(self, path, i, current_hash, psi, ctx):
        if i >= len(path):
            return self._check_psi(psi, current_hash, ctx)
        step = path[i]
        if step.is_event:
            for ev_h, _ in self.store.neighbors(current_hash):
                ev = self.store.get(ev_h)
                if ev["type"] != step.node_type: continue
                for out_h in self.store.event_outputs(ev_h):
                    if self._walk(path, i+1, out_h, psi, ctx): return True
            return False
        if self.store.artifact_types.get(current_hash) != step.node_type:
            return False
        return self._walk(path, i+1, current_hash, psi, ctx)

    def _eval_forall(self, node, endpoint, ctx):
        _, _, source, body = node
        chunks = ctx.get("retrieved_chunks", {}).get(endpoint, [])
        if not chunks: return False
        for c in chunks:
            if not self._walk(body[1], 0, c, body[2], ctx): return False
        return True

    def _resolve_start(self, endpoint):
        if endpoint in self.store.artifact_types: return [endpoint]
        if endpoint in self.store.store._log: return self.store.event_outputs(endpoint)
        return None

    def _check_psi(self, psi, ah, ctx):
        if psi is None: return True
        if isinstance(psi, tuple) and psi[0] == "psi_and":
            return self._check_psi(psi[1], ah, ctx) and self._check_psi(psi[2], ah, ctx)
        if isinstance(psi, tuple) and psi[0] == "psi_not":
            return not self._check_psi(psi[1], ah, ctx)
        meta = ctx.get("artifact_meta", {}).get(ah, {})
        return self._eval_atom(psi, meta)

    def _eval_atom(self, atom, meta):
        k = atom[0]
        if k == "eq":      return meta.get(f"{atom[1]}.{atom[2]}") == atom[3]
        if k == "in_":     return meta.get(f"{atom[1]}.{atom[2]}") in meta.get(f"__set__{atom[3]}", set())
        if k == "contains":return atom[3] in meta.get(f"{atom[1]}.{atom[2]}", [])
        if k == "allows":  return meta.get(f"{atom[1]}.{atom[2]}") == atom[3]
        if k == "is_certified": return bool(meta.get("certified"))
        if k == "no_unapproved_imports": return not meta.get("unapproved_imports", [])
        return False
