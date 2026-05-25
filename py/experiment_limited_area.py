import matplotlib.pyplot as plt
from utils import (
    DEFAULT_TRIALS, simulate_communication_limited_area, run_repeated_simulation
)

TRIALS = DEFAULT_TRIALS

# --------------------------
# 実験1: 限定領域 vs 全領域（N固定）
# --------------------------
print("=" * 60)
print("Experiment 1: Limited communication area comparison")
print("=" * 60)
print(f"Trials: {TRIALS}")

N = 100
AREA = 1000
COMMUNICATION_RANGE = 100

# 比較する領域サイズ（半辺長）
# 100×100領域 -> area_size=50
# 200×200領域 -> area_size=100
# etc.
area_sizes = [50, 100, 150]  # corresponding to 100×100, 200×200, 300×300

# 各領域サイズでシミュレーション（複数回平均）
exp1_results = {}
for area_size in area_sizes:
    area_label = f"{area_size*2}×{area_size*2}"
    
    times_no_spread, counts_no_spread = run_repeated_simulation(
        simulate_communication_limited_area, N, AREA, trials=TRIALS,
        seed_start=10000 + area_size, spread=False, 
        communication_range=COMMUNICATION_RANGE, area_size=area_size
    )
    
    times_spread, counts_spread = run_repeated_simulation(
        simulate_communication_limited_area, N, AREA, trials=TRIALS,
        seed_start=10000 + area_size, spread=True, 
        communication_range=COMMUNICATION_RANGE, area_size=area_size
    )
    
    exp1_results[area_size] = {
        'no_spread': (times_no_spread, counts_no_spread),
        'spread': (times_spread, counts_spread)
    }
    
    print(f"\n=== Limited area: {area_label} (comm_range={COMMUNICATION_RANGE}m) ===")
    print("No spread:")
    print(f"  Final average received: {counts_no_spread[-1]:.1f}/{N}")
    print("Spread enabled:")
    print(f"  Final average received: {counts_spread[-1]:.1f}/{N}")

# 全領域シミュレーション（area_size=None）
times_full_no_spread, counts_full_no_spread = run_repeated_simulation(
    simulate_communication_limited_area, N, AREA, trials=TRIALS,
    seed_start=19999, spread=False, 
    communication_range=COMMUNICATION_RANGE, area_size=None
)

times_full_spread, counts_full_spread = run_repeated_simulation(
    simulate_communication_limited_area, N, AREA, trials=TRIALS,
    seed_start=19999, spread=True, 
    communication_range=COMMUNICATION_RANGE, area_size=None
)

print(f"\n=== Full area (no limitation) ===")
print("No spread:")
print(f"  Final average received: {counts_full_no_spread[-1]:.1f}/{N}")
print("Spread enabled:")
print(f"  Final average received: {counts_full_spread[-1]:.1f}/{N}")

# 実験1のグラフ
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# No spread の比較
ax = axes[0]
for area_size in area_sizes:
    times, counts = exp1_results[area_size]['no_spread']
    area_label = f"{area_size*2}×{area_size*2}"
    ax.plot(times, counts, marker="o", label=area_label, linewidth=2)
ax.plot(times_full_no_spread, counts_full_no_spread, marker="s", 
        label="Full area", linewidth=2, linestyle="--", color="black")
ax.set_xlabel("Time", fontsize=11)
ax.set_ylabel("Average Received Nodes", fontsize=11)
ax.set_yticks(range(0, N + 1, 10))
ax.set_ylim(0, N + 1)
ax.grid(True, alpha=0.3)
ax.legend(fontsize=10)
ax.set_title("T0 only (No spread)", fontsize=12)

# Spread の比較
ax = axes[1]
for area_size in area_sizes:
    times, counts = exp1_results[area_size]['spread']
    area_label = f"{area_size*2}×{area_size*2}"
    ax.plot(times, counts, marker="o", label=area_label, linewidth=2)
ax.plot(times_full_spread, counts_full_spread, marker="s", 
        label="Full area", linewidth=2, linestyle="--", color="black")
ax.set_xlabel("Time", fontsize=11)
ax.set_ylabel("Average Received Nodes", fontsize=11)
ax.set_yticks(range(0, N + 1, 10))
ax.set_ylim(0, N + 1)
ax.grid(True, alpha=0.3)
ax.legend(fontsize=10)
ax.set_title("Received nodes also send (Spread)", fontsize=12)

plt.suptitle(f"Experiment 1: Limited area vs Full area (N={N}, comm_range={COMMUNICATION_RANGE}m, trials={TRIALS})", 
             fontsize=13, y=1.02)
plt.tight_layout()
plt.show()

# --------------------------
# 実験2: 固定Nで通信領域サイズ比較
# --------------------------
print("\n" + "=" * 60)
print("Experiment 2: Communication area size comparison (fixed N)")
print("=" * 60)
print(f"Trials: {TRIALS}")

N = 100
AREA = 1000
COMMUNICATION_RANGE = 100

# 領域サイズ（半辺長）
area_sizes_exp2 = [50, 75, 100, 125, 150]

exp2_results = {}
final_counts_no_spread = []
final_counts_spread = []

for area_size in area_sizes_exp2:
    times_no_spread, counts_no_spread = run_repeated_simulation(
        simulate_communication_limited_area, N, AREA, trials=TRIALS,
        seed_start=20000 + area_size, spread=False, 
        communication_range=COMMUNICATION_RANGE, area_size=area_size
    )
    
    times_spread, counts_spread = run_repeated_simulation(
        simulate_communication_limited_area, N, AREA, trials=TRIALS,
        seed_start=20000 + area_size, spread=True, 
        communication_range=COMMUNICATION_RANGE, area_size=area_size
    )
    
    exp2_results[area_size] = {
        'no_spread': (times_no_spread, counts_no_spread),
        'spread': (times_spread, counts_spread)
    }
    
    final_counts_no_spread.append(counts_no_spread[-1])
    final_counts_spread.append(counts_spread[-1])
    
    area_label = f"{area_size*2}×{area_size*2}"
    print(f"{area_label}: No spread={counts_no_spread[-1]:.1f}, Spread={counts_spread[-1]:.1f}")

# 実験2のグラフ
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# 時間変化
ax = axes[0]
for area_size in area_sizes_exp2:
    times, counts = exp2_results[area_size]['spread']
    area_label = f"{area_size*2}×{area_size*2}"
    ax.plot(times, counts, marker="o", label=area_label, linewidth=2)
ax.set_xlabel("Time", fontsize=11)
ax.set_ylabel("Average Received Nodes", fontsize=11)
ax.set_yticks(range(0, N + 1, 10))
ax.set_ylim(0, N + 1)
ax.grid(True, alpha=0.3)
ax.legend(fontsize=10)
ax.set_title("Time series (Spread enabled)", fontsize=12)

# 最終受信数比較
ax = axes[1]
area_labels = [f"{s*2}" for s in area_sizes_exp2]
x_pos = range(len(area_sizes_exp2))
ax.plot(x_pos, final_counts_no_spread, marker="o", label="No spread", linewidth=2, markersize=8)
ax.plot(x_pos, final_counts_spread, marker="s", label="Spread", linewidth=2, markersize=8)
ax.set_xticks(x_pos)
ax.set_xticklabels(area_labels)
ax.set_xlabel("Limited area size (width/height in m)", fontsize=11)
ax.set_ylabel("Final average received nodes", fontsize=11)
ax.set_yticks(range(0, N + 1, 10))
ax.set_ylim(0, N + 1)
ax.grid(True, alpha=0.3, axis='y')
ax.legend(fontsize=10)
ax.set_title("Final received count vs area size", fontsize=12)

plt.suptitle(f"Experiment 2: Area size comparison (N={N}, comm_range={COMMUNICATION_RANGE}m, trials={TRIALS})", 
             fontsize=13, y=1.02)
plt.tight_layout()
plt.show()

# --------------------------
# 実験3: 固定領域でノード数比較
# --------------------------
print("\n" + "=" * 60)
print("Experiment 3: Node count comparison (fixed area size)")
print("=" * 60)
print(f"Trials: {TRIALS}")

AREA = 1000
COMMUNICATION_RANGE = 100
AREA_SIZE = 100  # 200×200 area

node_counts = [20, 50, 100, 150, 200]

exp3_results = {}
final_counts_no_spread_exp3 = []
final_counts_spread_exp3 = []
received_rates_no_spread = []
received_rates_spread = []

for n in node_counts:
    times_no_spread, counts_no_spread = run_repeated_simulation(
        simulate_communication_limited_area, n, AREA, trials=TRIALS,
        seed_start=30000 + n, spread=False, 
        communication_range=COMMUNICATION_RANGE, area_size=AREA_SIZE
    )
    
    times_spread, counts_spread = run_repeated_simulation(
        simulate_communication_limited_area, n, AREA, trials=TRIALS,
        seed_start=30000 + n, spread=True, 
        communication_range=COMMUNICATION_RANGE, area_size=AREA_SIZE
    )
    
    exp3_results[n] = {
        'no_spread': (times_no_spread, counts_no_spread),
        'spread': (times_spread, counts_spread)
    }
    
    final_no_spread = counts_no_spread[-1]
    final_spread = counts_spread[-1]
    
    final_counts_no_spread_exp3.append(final_no_spread)
    final_counts_spread_exp3.append(final_spread)
    received_rates_no_spread.append(final_no_spread / n * 100)
    received_rates_spread.append(final_spread / n * 100)
    
    print(f"N={n}: No spread={final_no_spread:.1f}/{n} ({final_no_spread/n*100:.1f}%), "
          f"Spread={final_spread:.1f}/{n} ({final_spread/n*100:.1f}%)")

# 実験3のグラフ
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# 絶対受信数
ax = axes[0]
ax.plot(node_counts, final_counts_no_spread_exp3, marker="o", label="No spread", 
        linewidth=2, markersize=8)
ax.plot(node_counts, final_counts_spread_exp3, marker="s", label="Spread", 
        linewidth=2, markersize=8)
ax.set_xlabel("Number of nodes (N)", fontsize=11)
ax.set_ylabel("Final average received nodes", fontsize=11)
ax.grid(True, alpha=0.3)
ax.legend(fontsize=10)
ax.set_title("Absolute received count", fontsize=12)

# 受信率 (%)
ax = axes[1]
ax.plot(node_counts, received_rates_no_spread, marker="o", label="No spread", 
        linewidth=2, markersize=8)
ax.plot(node_counts, received_rates_spread, marker="s", label="Spread", 
        linewidth=2, markersize=8)
ax.set_xlabel("Number of nodes (N)", fontsize=11)
ax.set_ylabel("Received rate (%)", fontsize=11)
ax.set_ylim(0, 105)
ax.grid(True, alpha=0.3)
ax.legend(fontsize=10)
ax.set_title("Received rate comparison", fontsize=12)

plt.suptitle(f"Experiment 3: Node count comparison (area_size={AREA_SIZE*2}×{AREA_SIZE*2}m, comm_range={COMMUNICATION_RANGE}m, trials={TRIALS})", 
             fontsize=13, y=1.02)
plt.tight_layout()
plt.show()

print("\n" + "=" * 60)
print("All experiments completed!")
print("=" * 60)
