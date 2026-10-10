from __future__ import annotations
import json, tempfile, time
from pathlib import Path
from statistics import mean, stdev
from provml.integrity_store import IntegrityStore
from provml.query_store import QueryStore
from provml.supplyql.evaluator import BoundedPathEvaluator
from provml.enforcement.gateway import EnforcementGateway
from provml.events import Artifact, Event

def load_runs(path):
    return [json.loads(l) for l in Path(path).read_text().splitlines() if l.strip()]

def _to_event(ev):
    return Event(type=ev["type"], actor=ev["actor"],
                 inputs=[Artifact(**a) for a in ev["inputs"]],
                 outputs=[Artifact(**a) for a in ev["outputs"]],
                 parents=ev["parents"], seq=ev["seq"],
                 certificates=ev["certificates"])

def run_provml(run, policy=None, allowlist=None, witness_fn=lambda x: "local"):
    log_dir = tempfile.mkdtemp(prefix="provml-")
    store = IntegrityStore(log_dir=log_dir, witness_fn=witness_fn,
                           issuer_allowlist=allowlist or {})
    t0 = time.perf_counter()
    for ev in run["events"]:
        e = _to_event(ev); e.sig = ev.get("sig", "00")
        try: store.append(e, pk=None)
        except ValueError: pass
    store.force_seal()
    qs = QueryStore(store)
    ev_ = BoundedPathEvaluator(qs, kmax=6)
    gw = EnforcementGateway(ev_, mode="blocking")
    decision = gw.deploy_gate(policy, run)
    return {"decision": decision, "latency_ms": (time.perf_counter() - t0) * 1000}

def main():
    root = Path(__file__).resolve().parents[1] / "datasets"
    summary = {}
    for wf in ("w1_compile_load_deploy", "w2_rag_ingest_retrieve"):
        wf_dir = root / wf
        for cls in ("benign", "missing", "mismatched", "replayed", "forged"):
            path = wf_dir / (f"{cls}_runs.jsonl" if cls == "benign" else f"injected_{cls}.jsonl")
            if not path.exists(): continue
            runs = load_runs(path)
            decisions, latencies = [], []
            for r in runs:
                res = run_provml(r)
                decisions.append(res["decision"]); latencies.append(res["latency_ms"])
            summary[f"{wf}/{cls}"] = {
                "n": len(runs),
                "rejection_rate": decisions.count("BLOCK") / max(1, len(decisions)),
                "latency_mean_ms": mean(latencies) if latencies else 0.0,
                "latency_sd_ms": stdev(latencies) if len(latencies) > 1 else 0.0,
            }
    print(json.dumps(summary, indent=2))

if __name__ == "__main__":
    main()
