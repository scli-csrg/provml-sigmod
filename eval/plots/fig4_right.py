import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt, numpy as np
P = [50, 90, 95, 99, 99.9]
PROVML = [18, 46, 78, 118, 156]; BASE = [22, 52, 92, 134, 245]
x = np.arange(len(P)); w = 0.36
fig, ax = plt.subplots(figsize=(6, 3.2))
ax.bar(x-w/2, PROVML, w, label="ProvML", color="#444")
ax.bar(x+w/2, BASE,   w, label="composite baseline", color="#bbb")
ax.set_xticks(x); ax.set_xticklabels([f"p{p}" for p in P])
ax.set_ylabel("query latency (ms)"); ax.set_yscale("log"); ax.legend()
fig.tight_layout(); fig.savefig("fig4_right.pdf"); print("wrote fig4_right.pdf")
