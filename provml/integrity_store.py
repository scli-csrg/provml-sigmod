from __future__ import annotations
import json, threading, time
from pathlib import Path
from typing import Callable, Dict, List, Optional
from .commitment import event_commitment, batch_merkle_root
from .events import Event

class IntegrityStore:
    def __init__(self, log_dir, witness_fn, batch_max=4096, seal_interval_s=60.0, issuer_allowlist=None):
        self.log_dir = Path(log_dir); self.log_dir.mkdir(parents=True, exist_ok=True)
        self.witness_fn = witness_fn; self.batch_max = batch_max
        self.seal_interval_s = seal_interval_s
        self.issuer_allowlist = issuer_allowlist or {}
        self._lock = threading.RLock()
        self._log = {}; self._seq = {}; self._heads = {}
        self._batch = []; self._last_seal = time.time(); self._seals = []
        self._load_existing()

    def _load_existing(self):
        path = self.log_dir / "log.jsonl"
        if path.exists():
            for line in path.read_text().splitlines():
                rec = json.loads(line)
                self._log[rec["h"]] = rec["event"]
                self._seq[rec["event"]["actor"]] = rec["event"]["seq"]

    def _append_log(self, h, event):
        with (self.log_dir / "log.jsonl").open("a") as f:
            f.write(json.dumps({"h": h, "event": event}) + "\n")

    def append(self, event, pk=None):
        with self._lock:
            event.validate_schema()
            d = event.to_dict()
            h = event_commitment(d)
            if h in self._log:
                return h
            if pk is not None and not event.verify(pk):
                return "REJECT:sig"
            if event.seq <= self._seq.get(event.actor, -1):
                return "REJECT:replay"
            for cert in event.certificates:
                allowed = self.issuer_allowlist.get(event.type, set())
                if allowed and cert.get("issuer") not in allowed:
                    return "REJECT:issuer"
            for art in event.inputs:
                if not self._recheck_bytes(art):
                    return "REJECT:bytes"
            parent_key = ",".join(sorted(event.parents)) or "__root__"
            if not self._cas_head(parent_key, h):
                event.parents = [self._heads[parent_key]]
                return self.append(event, pk)
            self._log[h] = d; self._seq[event.actor] = event.seq
            self._heads[parent_key] = h
            self._append_log(h, d); self._batch.append(h)
            if len(self._batch) >= self.batch_max or self._seal_timer_fired():
                self._seal_batch()
            return h

    def _recheck_bytes(self, art): return True
    def _cas_head(self, key, h): return key not in self._heads or self._heads[key] != h
    def _seal_timer_fired(self): return (time.time() - self._last_seal) >= self.seal_interval_s

    def _seal_batch(self):
        if not self._batch: return {}
        root = batch_merkle_root(self._batch)
        witness = self.witness_fn(root)
        seal = {"merkle_root": root, "event_count": len(self._batch),
                "witness": witness, "sealed_at": time.time()}
        self._seals.append(seal)
        with (self.log_dir / "seals.jsonl").open("a") as f:
            f.write(json.dumps(seal) + "\n")
        self._batch = []; self._last_seal = time.time()
        return seal

    def force_seal(self):
        with self._lock:
            return self._seal_batch()

    def get(self, h): return self._log.get(h)
    def all_events(self): return list(self._log.values())
    @property
    def seals(self): return list(self._seals)
