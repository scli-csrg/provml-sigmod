from __future__ import annotations
import math, tempfile, time
from provml.integrity_store import IntegrityStore
from provml.query_store import QueryStore
from provml.events import Artifact, Event

def synthesize_events(n):
    prev = []
    for i in range(n):
        a_in  = Artifact(hash=f"{i:064x}",   type="Checkpoint", role="in",  size=1024)
        a_out = Artifact(hash=f"{i+1:064x}", type="Binary",     role="out", size=1024)
        e = Event(type="Compile", actor=f"actor{i%16}", inputs=[a_in],
                  outputs=[a_out], parents=prev[-1:] if prev else [], seq=i,
                  certificates=[{"kind":"compiler_hash","issuer":"ci","value":"xla"},
                                {"kind":"flags","issuer":"ci","value":"-O2"},
                                {"kind":"post_compile_equivalence","issuer":"ci","value":"pass"}])
        prev.append(e.commitment)
        yield e

def measure(n):
    log_dir = tempfile.mkdtemp(prefix="provml-scale-")
    store = IntegrityStore(log_dir, witness_fn=lambda x: "w", batch_max=10**9)
    t0 = time.perf_counter()
    for e in synthesize_events(n):
        store._log[e.commitment] = e.to_dict()
    store.force_seal(); QueryStore(store)
    return (time.perf_counter() - t0) * 1000.0

def main():
    sizes = [10**3, 10**4, 10**5, 10**6]
    times = [measure(n) for n in sizes]
    xs = [math.log10(n) for n in sizes]; ys = [math.log10(t) for t in times]
    n = len(xs); mx = sum(xs)/n; my = sum(ys)/n
    ss_xx = sum((x-mx)**2 for x in xs); ss_yy = sum((y-my)**2 for y in ys)
    ss_xy = sum((x-mx)*(y-my) for x, y in zip(xs, ys))
    print(f"sizes={sizes}\ntimes_ms={times}\nslope={ss_xy/ss_xx:.3f} R2={(ss_xy**2)/(ss_xx*ss_yy):.3f}")

if __name__ == "__main__":
    main()
