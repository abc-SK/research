#通信距離や情報拡散の仕組みによって、情報を受取る端末数がどう変わるか

import matplotlib.pyplot as plt
from utils import (
    DEFAULT_TRIALS, simulate_communication, run_repeated_simulation
)

#DEFAULT_TRIALS は、何回シミュレーションを繰り返すか。今は utils.py で 20 に設定。
#simulate_communication は、1回分の通信シミュレーションを行う関数。
#run_repeated_simulation は、同じ条件のシミュレーションを複数回行い、平均を出す関数。

# --------------------------
# パラメータ
# --------------------------
N = 20
AREA = 1000 #1000*1000
COMMUNICATION_RANGES = [50, 100, 150]
TRIALS = DEFAULT_TRIALS

# --------------------------
# シミュレーション関数
# --------------------------
# （現在 utils からインポート）

# --------------------------
# シミュレーション実行（複数回平均）
# --------------------------
results = {}
for r in COMMUNICATION_RANGES:
    # T0のみ
    results[(r, False)] = run_repeated_simulation(
        simulate_communication, N, AREA, trials=TRIALS,
        seed_start=1000 + r, spread=False, communication_range=r
    )
    # 拡散あり
    results[(r, True)] = run_repeated_simulation(
        simulate_communication, N, AREA, trials=TRIALS,
        seed_start=1000 + r, spread=True, communication_range=r
    )

# 結果表示
print(f"Trials: {TRIALS}")
for r in COMMUNICATION_RANGES: #r=50,100,150
    times_no_spread, counts_no_spread = results[(r, False)]
    times_spread, counts_spread = results[(r, True)]

    print(f"\n=== Communication range {r}m ===")
    print("=== T0 only (no spread) ===")
    for t, c in zip(times_no_spread, counts_no_spread):
        print(f"time: {t}, average received: {c:.1f}")

    print("\n=== Received nodes also send (spread enabled) ===")
    for t, c in zip(times_spread, counts_spread):
        print(f"time: {t}, average received: {c:.1f}")

# --------------------------
# グラフ（比較）
# --------------------------
plt.figure(figsize=(10, 6))

for r in COMMUNICATION_RANGES:
    times_no_spread, counts_no_spread = results[(r, False)]
    times_spread, counts_spread = results[(r, True)]

    plt.plot(times_no_spread, counts_no_spread, marker="o", label=f"{r}m : T0 only", linewidth=2)
    plt.plot(times_spread, counts_spread, marker="s", linestyle="--", label=f"{r}m : Spread", linewidth=2)

plt.xlabel("Time", fontsize=12)
plt.ylabel("Average Received Nodes", fontsize=12)
plt.yticks(range(0, N + 1))
plt.ylim(0, N + 1)
plt.grid(True, alpha=0.3)
plt.legend(fontsize=11)
plt.title(f"Communication mode comparison (average of {TRIALS} trials)", fontsize=14)
plt.tight_layout()
plt.show()
