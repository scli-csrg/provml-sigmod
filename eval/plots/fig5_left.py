import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt, numpy as np
sizes = np.array([1e3,1e4,1e5,1e6,1e7])
provml = np.array([15,32,71,148,312]); base = np.array([18,41,96,221,498])
fig, ax = plt.subplots(figsize=(5, 3.2))
ax.loglog(sizes, provml, "o-", color="#222", label="ProvML")
ax.loglog(sizes, base,   "s--", color="#888", label="composite baseline")
ax.set_xlabel("events"); ax.set_ylabel("trace latency (ms)"); ax.legend()
fig.tight_layout(); fig.savefig("fig5_left.pdf"); print("wrote fig5_left.pdf")
