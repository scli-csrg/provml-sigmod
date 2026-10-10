import json
from pathlib import Path
def table5(raw):
    rows = ["class                         rejection  latency_ms"]
    for k, v in raw.items():
        rows.append(f"{k:28s} {v['rejection_rate']:.3f}      {v['latency_mean_ms']:.1f}")
    return "\n".join(rows)
if __name__ == "__main__":
    src = Path("harness_output.json")
    if src.exists():
        print(table5(json.loads(src.read_text())))
    else:
        print("run `python -m eval.harness > harness_output.json` first")
