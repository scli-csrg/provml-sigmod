import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt, numpy as np
names = ["RAG vec","RAG chunk","Compiler IR","ResNet-50 ckpt","Compiled bin","BERT-base ckpt","Package"]
hash_pct = [66.7,50.0,80.0,61.6,59.8,62.1,60.3]
sign_pct = [33.3,37.5,16.7,24.4,28.7,25.1,27.6]
idx_pct  = [33.3,25.0, 6.7,11.6,12.4,10.6,12.1]
x = np.arange(len(names)); w = 0.26
fig, ax = plt.subplots(figsize=(6, 3.2))
ax.bar(x-w, hash_pct, w, label="hash",  color="#333")
ax.bar(x,   sign_pct, w, label="sign",  color="#777")
ax.bar(x+w, idx_pct,  w, label="index", color="#bbb")
ax.set_xticks(x); ax.set_xticklabels(names, rotation=30, ha="right")
ax.set_ylabel("overhead (% of base step)"); ax.legend()
fig.tight_layout(); fig.savefig("fig5_right.pdf"); print("wrote fig5_right.pdf")
