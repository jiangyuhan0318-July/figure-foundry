"""Generate an explicitly synthetic, seeded demonstration dataset."""
import csv
from pathlib import Path
import numpy as np

SEED = 20261026
METHODS = ["Baseline", "Variant A", "Variant B"]


def main():
    rng = np.random.default_rng(SEED)
    epochs = np.arange(0, 101, 5)
    rows = []
    for run in range(1, 9):
        shared_offset = rng.normal(0, 0.65)
        shared_latency = rng.normal(0, 0.20)
        for index, method in enumerate(METHODS):
            target = [88.3, 90.8, 93.3][index] + shared_offset + rng.normal(0, 0.40)
            tau = [21.0, 19.0, 17.5][index] + rng.normal(0, 0.7)
            scores = target - 50 * np.exp(-epochs / tau)
            scores += rng.normal(0, 0.25, size=len(epochs))
            latency = [7.9, 9.35, 10.9][index] + shared_latency + rng.normal(0, 0.12)
            for epoch, score in zip(epochs, scores):
                rows.append([method, f"run-{run:02d}", int(epoch), float(score), float(latency), "synthetic"])
    output = Path(__file__).with_name("synthetic_data.csv")
    with output.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.writer(stream, lineterminator="\n")
        writer.writerow(["method", "run_id", "epoch", "score_pct", "latency_ms", "data_kind"])
        writer.writerows(rows)
    print(f"Synthetic seed={SEED}; {len(rows)} rows; 3 methods x 8 runs x 21 checkpoints")


if __name__ == "__main__":
    main()
