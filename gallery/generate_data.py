"""Create seeded synthetic inputs for 24 FigureFoundry gallery examples."""
import json
from pathlib import Path
import numpy as np

SEED = 261026


def main():
    r = np.random.default_rng(SEED)
    d = {"synthetic": True, "seed": SEED, "description": "Educational synthetic data and toy schematic relationships; no real experiments."}
    d["grouped_bar"] = r.normal(np.array([[62, 70, 75], [68, 77, 82], [72, 80, 87], [65, 74, 79]])[:, :, None], 3, (4, 3, 8))
    time = np.arange(25)
    d["trend"] = {"time": time, "values": np.stack([25 + 4*i + .4*time + 3*np.sin(time/4 + i/3) + r.normal(0, 1.5, (8, 25)) for i in range(3)])}
    before = r.normal(45, 7, 14)
    d["paired"] = {"before": before, "after": before + r.normal(9, 4, 14)}
    d["forest"] = r.normal(np.array([-1.0, .2, 1.4, 2.5, 3.1, 4.2])[:, None], 1.7, (6, 12))
    d["lollipop"] = np.sort(r.uniform(12, 85, 8))
    d["waterfall"] = {"start": 100, "changes": [24, -11, 18, -9]}
    d["distributions"] = [r.normal(9 + i*2, 1 + i*.3, 60) for i in range(3)]
    d["ridge"] = [r.normal(i*.9, .7 + .1*i, 120) for i in range(5)]
    x = r.uniform(0, 10, 90)
    d["regression"] = {"x": x, "y": 2.4 + 1.5*x + r.normal(0, 2.1, len(x))}
    d["bubble"] = {"x": r.uniform(2, 12, 18), "y": r.uniform(15, 85, 18), "size": r.uniform(10, 100, 18), "group": np.arange(18)%3}
    latent = r.normal(size=(100, 3))
    load = np.array([[1, .1, 0], [.9, .2, 0], [.1, 1, .2], [0, .8, .4], [-.8, .1, .2], [.2, -.6, .7]])
    d["correlation_inputs"] = latent @ load.T + r.normal(0, .35, (100, 6))
    groups = np.repeat(np.arange(3), 45)
    centers = np.array([[-2, 1, 0, 1, 0, .3], [1.5, 2, 1, 0, 0, -.5], [1, -2, -.5, -.3, 1, .5]])
    d["pca"] = {"x": centers[groups] + r.normal(0, .7, (135, 6)), "group": groups}
    truth = np.array([1]*120 + [0]*280)
    scores = np.stack([1/(1+np.exp(-((truth*2-1)*mu + r.normal(0, 1, len(truth))))) for mu in [.6, .9, 1.2]])
    d["classification"] = {"truth": truth, "scores": scores}
    genes = 160
    base = r.normal(6, .7, genes)
    effect = np.zeros(genes); effect[:22] = -1.4; effect[22:44] = 1.5
    d["volcano"] = {"control": base[:, None] + r.normal(0, .7, (genes, 12)), "treated": (base+effect)[:, None] + r.normal(0, .7, (genes, 12))}
    survival = []
    for hazard in [.18, .12, .075]:
        events = r.exponential(1/hazard, 60); censor = r.uniform(6, 18, 60)
        survival.append({"time": np.minimum(events, censor), "event": (events <= censor).astype(int)})
    d["survival"] = survival
    d["composition"] = np.stack([r.dirichlet(a, 10) for a in [[4, 2, 2], [2, 4, 2], [2, 2, 5], [3, 3, 3]]])
    t = np.linspace(0, 24, 49)
    raw = np.array([2+np.sin(t/5), 1.5+.6*np.cos(t/4), 1+.04*t])
    d["area"] = {"time": t, "fractions": raw/raw.sum(axis=0)}
    d["radar"] = {"labels": ["Accuracy", "Stability", "Speed", "Robustness", "Efficiency"], "scores": [[78, 74, 89, 65, 84], [85, 82, 76, 81, 78], [92, 89, 69, 90, 72]]}
    d["network"] = {"labels": list("ABCDEFG"), "positions": [[.5+.33*np.cos(a), .5+.33*np.sin(a)] for a in np.linspace(0, 2*np.pi, 6, endpoint=False)]+[[.5, .5]], "edges": [[0,1,1.2],[1,2,.9],[2,3,1.6],[3,4,.8],[4,5,1.1],[5,0,1.5],[6,0,1.1],[6,2,1.4],[6,4,.9]]}
    d["flowchart"] = {"nodes": ["Input table", "Check units", "Valid?", "Plot + export", "Fix data"], "edges": [[0,1,"next"],[1,2,"next"],[2,3,"yes"],[2,4,"no"],[4,1,"retry"]]}
    d["architecture"] = {"nodes": ["Input", "Encoder A", "Encoder B", "Fusion", "Prediction", "Labels", "Loss"], "data_edges": [[0,1],[0,2],[1,3],[2,3],[3,4]], "training_edges": [[4,6],[5,6]]}
    folder = Path(__file__).resolve().parent
    (folder/"synthetic_data.json").write_text(json.dumps(d, default=lambda x: x.tolist(), indent=2)+"\n", encoding="utf-8")
    print(f"Saved synthetic gallery data, seed={SEED}; 24 chart/diagram examples.")


if __name__ == "__main__":
    main()
