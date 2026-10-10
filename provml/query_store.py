from __future__ import annotations
from collections import defaultdict
from typing import Dict, List, Tuple
from .integrity_store import IntegrityStore

class QueryStore:
    def __init__(self, store: IntegrityStore):
        self.store = store
        self.by_artifact = defaultdict(list); self.by_event_type = defaultdict(list)
        self.by_actor = defaultdict(list); self.artifact_types = {}
        self.rebuild()

    def rebuild(self):
        self.by_artifact.clear(); self.by_event_type.clear(); self.by_actor.clear()
        for h, ev in self.store._log.items():
            self.by_event_type[ev["type"]].append(h)
            self.by_actor[ev["actor"]].append(h)
            for a in ev["inputs"] + ev["outputs"]:
                self.by_artifact[a["hash"]].append(h)
                self.artifact_types[a["hash"]] = a["type"]

    def neighbors(self, artifact_hash):
        out = []
        for h in self.by_artifact.get(artifact_hash, []):
            ev = self.store.get(h)
            for a in ev["inputs"]:
                if a["hash"] == artifact_hash: out.append((h, "input"))
            for a in ev["outputs"]:
                if a["hash"] == artifact_hash: out.append((h, "output"))
        return out

    def event_outputs(self, event_hash):
        return [a["hash"] for a in self.store.get(event_hash)["outputs"]]

    def event_inputs(self, event_hash):
        return [a["hash"] for a in self.store.get(event_hash)["inputs"]]
