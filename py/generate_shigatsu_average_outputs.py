import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from utils import (
    DEFAULT_TRIALS,
    MINIMUM_DISTANCE,
    SPEED,
    TIME,
)


OUT_DIR = Path("output_shigatsu")
OUT_DIR.mkdir(exist_ok=True)


def distance(a, b):
    dx = a[0] - b[0]
    dy = a[1] - b[1]
    return (dx * dx + dy * dy) ** 0.5


def is_far_enough(point, points, min_dist):
    return all(distance(point, p) >= min_dist for p in points)


def generate_points(n, area, rng, max_attempts=10000):
    points = []
    attempts = 0
    while len(points) < n and attempts < max_attempts:
        point = [rng.uniform(0, area), rng.uniform(0, area)]
        if is_far_enough(point, points, MINIMUM_DISTANCE):
            points.append(point)
        attempts += 1
    if len(points) < n:
        raise ValueError(f"Could not place {n} points in area {area}.")
    return np.array(points, dtype=float)


def simulate_fast(nodes, targets, n, area, rng, spread=False, communication_range=100, area_size=None):
    nodes = nodes.copy()
    targets = targets.copy()
    received = np.zeros(n, dtype=bool)
    received[0] = True
    times = []
    counts = []
    center = area / 2
    range_sq = communication_range * communication_range

    for t in range(TIME):
        delta = targets - nodes
        dist = np.linalg.norm(delta, axis=1)
        moving = dist > SPEED
        nodes[moving] += SPEED * delta[moving] / dist[moving, None]

        arrived_indexes = np.where(~moving)[0]
        for i in arrived_indexes:
            nodes[i] = targets[i]
            while True:
                new_target = [rng.uniform(0, area), rng.uniform(0, area)]
                if is_far_enough(new_target, targets.tolist(), MINIMUM_DISTANCE):
                    targets[i] = new_target
                    break

        if area_size is None:
            area_mask = np.ones(n, dtype=bool)
        else:
            area_mask = (
                (center - area_size <= nodes[:, 0])
                & (nodes[:, 0] <= center + area_size)
                & (center - area_size <= nodes[:, 1])
                & (nodes[:, 1] <= center + area_size)
            )

        if not spread:
            if area_mask[0]:
                diff = nodes - nodes[0]
                within = np.sum(diff * diff, axis=1) <= range_sq
                received |= within & area_mask
        else:
            active = received & area_mask
            if np.any(active):
                diff = nodes[:, None, :] - nodes[None, :, :]
                edges = np.sum(diff * diff, axis=2) <= range_sq
                edges &= area_mask[:, None] & area_mask[None, :]
                reachable = active.copy()
                frontier = active.copy()
                while np.any(frontier):
                    neighbors = np.any(edges[frontier], axis=0)
                    new_frontier = neighbors & ~reachable
                    if not np.any(new_frontier):
                        break
                    reachable |= new_frontier
                    frontier = new_frontier
                received |= reachable

        current_time = t + 1
        if current_time % 100 == 0:
            times.append(current_time)
            counts.append(float(np.sum(received)))

    return times, counts


def run_repeated_simulation_fast(n, area, trials=DEFAULT_TRIALS, seed_start=0, **simulation_kwargs):
    all_counts = []
    times = None
    for trial in range(trials):
        placement_rng = __import__("random").Random(seed_start + trial)
        movement_rng = __import__("random").Random(seed_start + 100000 + trial)
        nodes = generate_points(n, area, placement_rng)
        targets = generate_points(n, area, placement_rng)
        trial_times, trial_counts = simulate_fast(
            nodes, targets, n, area, movement_rng, **simulation_kwargs
        )
        if times is None:
            times = trial_times
        all_counts.append(trial_counts)
    return times, [sum(values) / len(values) for values in zip(*all_counts)]


def series_to_dict(times, counts):
    return {"times": times, "counts": [round(c, 3) for c in counts]}


def run_non_comm_area():
    n = 20
    area = 1000
    communication_ranges = [50, 100, 150]
    results = {}

    for r in communication_ranges:
        results[f"{r}_no_spread"] = run_repeated_simulation_fast(
            n,
            area,
            trials=DEFAULT_TRIALS,
            seed_start=1000 + r,
            spread=False,
            communication_range=r,
        )
        results[f"{r}_spread"] = run_repeated_simulation_fast(
            n,
            area,
            trials=DEFAULT_TRIALS,
            seed_start=1000 + r,
            spread=True,
            communication_range=r,
        )

    plt.figure(figsize=(10, 6))
    for r in communication_ranges:
        times, counts = results[f"{r}_no_spread"]
        plt.plot(times, counts, marker="o", label=f"{r}m : T0 only", linewidth=2)
        times, counts = results[f"{r}_spread"]
        plt.plot(times, counts, marker="s", linestyle="--", label=f"{r}m : Spread", linewidth=2)

    plt.xlabel("Time", fontsize=12)
    plt.ylabel("Average Received Nodes", fontsize=12)
    plt.yticks(range(0, n + 1))
    plt.ylim(0, n + 1)
    plt.grid(True, alpha=0.3)
    plt.legend(fontsize=11)
    plt.title(f"Communication mode comparison (average of {DEFAULT_TRIALS} trials)", fontsize=14)
    plt.tight_layout()
    plt.savefig(OUT_DIR / "average_non_comm_area.png", dpi=160)
    plt.close()

    return {
        "n": n,
        "area": area,
        "communication_ranges": communication_ranges,
        "results": {key: series_to_dict(*value) for key, value in results.items()},
    }


def run_experiment_limited_area():
    area = 1000
    communication_range = 100
    n = 100

    area_sizes_exp1 = [50, 100, 150]
    exp1_results = {}
    for area_size in area_sizes_exp1:
        exp1_results[f"{area_size}_no_spread"] = run_repeated_simulation_fast(
            n,
            area,
            trials=DEFAULT_TRIALS,
            seed_start=10000 + area_size,
            spread=False,
            communication_range=communication_range,
            area_size=area_size,
        )
        exp1_results[f"{area_size}_spread"] = run_repeated_simulation_fast(
            n,
            area,
            trials=DEFAULT_TRIALS,
            seed_start=10000 + area_size,
            spread=True,
            communication_range=communication_range,
            area_size=area_size,
        )

    full_no_spread = run_repeated_simulation_fast(
        n,
        area,
        trials=DEFAULT_TRIALS,
        seed_start=19999,
        spread=False,
        communication_range=communication_range,
        area_size=None,
    )
    full_spread = run_repeated_simulation_fast(
        n,
        area,
        trials=DEFAULT_TRIALS,
        seed_start=19999,
        spread=True,
        communication_range=communication_range,
        area_size=None,
    )

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    ax = axes[0]
    for area_size in area_sizes_exp1:
        times, counts = exp1_results[f"{area_size}_no_spread"]
        ax.plot(times, counts, marker="o", label=f"{area_size * 2}×{area_size * 2}", linewidth=2)
    ax.plot(full_no_spread[0], full_no_spread[1], marker="s", label="Full area", linewidth=2, linestyle="--", color="black")
    ax.set_xlabel("Time", fontsize=11)
    ax.set_ylabel("Average Received Nodes", fontsize=11)
    ax.set_yticks(range(0, n + 1, 10))
    ax.set_ylim(0, n + 1)
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=10)
    ax.set_title("T0 only (No spread)", fontsize=12)

    ax = axes[1]
    for area_size in area_sizes_exp1:
        times, counts = exp1_results[f"{area_size}_spread"]
        ax.plot(times, counts, marker="o", label=f"{area_size * 2}×{area_size * 2}", linewidth=2)
    ax.plot(full_spread[0], full_spread[1], marker="s", label="Full area", linewidth=2, linestyle="--", color="black")
    ax.set_xlabel("Time", fontsize=11)
    ax.set_ylabel("Average Received Nodes", fontsize=11)
    ax.set_yticks(range(0, n + 1, 10))
    ax.set_ylim(0, n + 1)
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=10)
    ax.set_title("Received nodes also send (Spread)", fontsize=12)

    plt.suptitle(
        f"Experiment 1: Limited area vs Full area (N={n}, comm_range={communication_range}m, trials={DEFAULT_TRIALS})",
        fontsize=13,
        y=1.02,
    )
    plt.tight_layout()
    plt.savefig(OUT_DIR / "average_limited_area_exp1.png", dpi=160)
    plt.close()

    area_sizes_exp2 = [50, 75, 100, 125, 150]
    exp2_results = {}
    final_counts_no_spread = []
    final_counts_spread = []
    for area_size in area_sizes_exp2:
        no_spread = run_repeated_simulation_fast(
            n,
            area,
            trials=DEFAULT_TRIALS,
            seed_start=20000 + area_size,
            spread=False,
            communication_range=communication_range,
            area_size=area_size,
        )
        spread = run_repeated_simulation_fast(
            n,
            area,
            trials=DEFAULT_TRIALS,
            seed_start=20000 + area_size,
            spread=True,
            communication_range=communication_range,
            area_size=area_size,
        )
        exp2_results[f"{area_size}_no_spread"] = no_spread
        exp2_results[f"{area_size}_spread"] = spread
        final_counts_no_spread.append(no_spread[1][-1])
        final_counts_spread.append(spread[1][-1])

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    ax = axes[0]
    for area_size in area_sizes_exp2:
        times, counts = exp2_results[f"{area_size}_spread"]
        ax.plot(times, counts, marker="o", label=f"{area_size * 2}×{area_size * 2}", linewidth=2)
    ax.set_xlabel("Time", fontsize=11)
    ax.set_ylabel("Average Received Nodes", fontsize=11)
    ax.set_yticks(range(0, n + 1, 10))
    ax.set_ylim(0, n + 1)
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=10)
    ax.set_title("Time series (Spread enabled)", fontsize=12)

    ax = axes[1]
    area_labels = [f"{s * 2}" for s in area_sizes_exp2]
    x_pos = range(len(area_sizes_exp2))
    ax.plot(x_pos, final_counts_no_spread, marker="o", label="No spread", linewidth=2, markersize=8)
    ax.plot(x_pos, final_counts_spread, marker="s", label="Spread", linewidth=2, markersize=8)
    ax.set_xticks(x_pos)
    ax.set_xticklabels(area_labels)
    ax.set_xlabel("Limited area size (width/height in m)", fontsize=11)
    ax.set_ylabel("Final average received nodes", fontsize=11)
    ax.set_yticks(range(0, n + 1, 10))
    ax.set_ylim(0, n + 1)
    ax.grid(True, alpha=0.3, axis="y")
    ax.legend(fontsize=10)
    ax.set_title("Final average received count vs area size", fontsize=12)

    plt.suptitle(
        f"Experiment 2: Area size comparison (N={n}, comm_range={communication_range}m, trials={DEFAULT_TRIALS})",
        fontsize=13,
        y=1.02,
    )
    plt.tight_layout()
    plt.savefig(OUT_DIR / "average_area_size_exp2.png", dpi=160)
    plt.close()

    node_counts = [20, 50, 100, 150, 200]
    area_size = 100
    exp3_results = {}
    final_counts_no_spread_exp3 = []
    final_counts_spread_exp3 = []
    received_rates_no_spread = []
    received_rates_spread = []
    for node_count in node_counts:
        no_spread = run_repeated_simulation_fast(
            node_count,
            area,
            trials=DEFAULT_TRIALS,
            seed_start=30000 + node_count,
            spread=False,
            communication_range=communication_range,
            area_size=area_size,
        )
        spread = run_repeated_simulation_fast(
            node_count,
            area,
            trials=DEFAULT_TRIALS,
            seed_start=30000 + node_count,
            spread=True,
            communication_range=communication_range,
            area_size=area_size,
        )
        exp3_results[f"{node_count}_no_spread"] = no_spread
        exp3_results[f"{node_count}_spread"] = spread
        final_no_spread = no_spread[1][-1]
        final_spread = spread[1][-1]
        final_counts_no_spread_exp3.append(final_no_spread)
        final_counts_spread_exp3.append(final_spread)
        received_rates_no_spread.append(final_no_spread / node_count * 100)
        received_rates_spread.append(final_spread / node_count * 100)

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    ax = axes[0]
    ax.plot(node_counts, final_counts_no_spread_exp3, marker="o", label="No spread", linewidth=2, markersize=8)
    ax.plot(node_counts, final_counts_spread_exp3, marker="s", label="Spread", linewidth=2, markersize=8)
    ax.set_xlabel("Number of nodes (N)", fontsize=11)
    ax.set_ylabel("Final average received nodes", fontsize=11)
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=10)
    ax.set_title("Absolute received count", fontsize=12)

    ax = axes[1]
    ax.plot(node_counts, received_rates_no_spread, marker="o", label="No spread", linewidth=2, markersize=8)
    ax.plot(node_counts, received_rates_spread, marker="s", label="Spread", linewidth=2, markersize=8)
    ax.set_xlabel("Number of nodes (N)", fontsize=11)
    ax.set_ylabel("Average received rate (%)", fontsize=11)
    ax.set_ylim(0, 105)
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=10)
    ax.set_title("Received rate comparison", fontsize=12)

    plt.suptitle(
        f"Experiment 3: Node count comparison (area_size={area_size * 2}×{area_size * 2}m, comm_range={communication_range}m, trials={DEFAULT_TRIALS})",
        fontsize=13,
        y=1.02,
    )
    plt.tight_layout()
    plt.savefig(OUT_DIR / "average_node_count_exp3.png", dpi=160)
    plt.close()

    return {
        "n": n,
        "area": area,
        "communication_range": communication_range,
        "area_sizes_exp1": area_sizes_exp1,
        "area_sizes_exp2": area_sizes_exp2,
        "node_counts": node_counts,
        "area_size_exp3": area_size,
        "exp1": {
            **{key: series_to_dict(*value) for key, value in exp1_results.items()},
            "full_no_spread": series_to_dict(*full_no_spread),
            "full_spread": series_to_dict(*full_spread),
        },
        "exp2": {key: series_to_dict(*value) for key, value in exp2_results.items()},
        "exp3": {key: series_to_dict(*value) for key, value in exp3_results.items()},
    }


def main():
    data = {
        "trials": DEFAULT_TRIALS,
        "non_comm_area": run_non_comm_area(),
        "limited_area": run_experiment_limited_area(),
    }
    out_path = OUT_DIR / "shigatsu_average_results.json"
    out_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(out_path)


if __name__ == "__main__":
    main()
