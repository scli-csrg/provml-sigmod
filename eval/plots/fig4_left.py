import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
x = [0,5,10,15,20,25,30,35,40,45,50]
w1 = [1.000,0.999,0.997,0.995,0.993,0.991,0.988,0.985,0.983,0.981,0.977]
w2 = [1.000,0.999,0.997,0.995,0.993,0.990,0.987,0.984,0.982,0.979,0.976]
fig, ax = plt.subplots(figsize=(5, 3.2))
ax.plot(x, w1, color="#222", label="W1"); ax.plot(x, w2, color="#222", linestyle="--", label="W2")
ax.set_xlabel("corrupted fraction of graph (%)"); ax.set_ylabel("rejection rate"); ax.legend()
fig.tight_layout(); fig.savefig("fig4_left.pdf"); print("wrote fig4_left.pdf")
