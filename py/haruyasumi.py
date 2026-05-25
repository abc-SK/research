import random
import matplotlib.pyplot as plt
import math

N = 100
TRIALS = 200

Ps = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]

#それぞれのPに対して平均と分散を格納するリスト
avg_list = []
var_list = []

# 図をまとめて表示（行数と列数を動的に決定）4×3のグラフ
num_plots = len(Ps) + 1  # ヒストグラム + P vs 分散グラフ
cols = 3 #横に3列で表示
rows = math.ceil(num_plots / cols)

plt.figure(figsize=(15, 4*rows))

for idx, P in enumerate(Ps):
    results = []

    # --------------------------
    # グラフ生成
    # --------------------------
    edges = []
    for i in range(N):
        for j in range(i+1, N):
            if random.random() < P:
                edges.append((i, j))

    adj = [[0]*N for _ in range(N)]
    for a, b in edges:
        adj[a][b] = 1
        adj[b][a] = 1

    # --------------------------
    # 貪欲彩色
    # --------------------------
    def greedy_coloring(order):
        color = [0]*N
        for v in order:
            used = [0]*(N+1)
            for u in range(N):
                if adj[v][u] == 1 and color[u] != 0:
                    used[color[u]] = 1
            c = 1
            while used[c] == 1:
                c += 1
            color[v] = c
        return max(color)

    # --------------------------
    # シミュレーション
    # --------------------------
    for _ in range(TRIALS):
        order = list(range(N))
        random.shuffle(order)
        results.append(greedy_coloring(order))

    # --------------------------
    # 平均と分散
    # --------------------------
    avg = sum(results) / TRIALS
    var = sum((x - avg)**2 for x in results) / TRIALS

    avg_list.append(avg)
    var_list.append(var)

    print(f"P = {P}")
    print("平均:", avg)
    print("分散:", var)
    print("--------------------")

    # --------------------------
    # ヒストグラム（分布）
    # --------------------------
    plt.subplot(rows, cols, idx+1)
    plt.hist(results, bins=range(min(results), max(results)+2), edgecolor='black')
    plt.title(f"P={P}")
    plt.xlabel("colors")
    plt.ylabel("count")

# --------------------------
# P vs 分散グラフ
# --------------------------
plt.subplot(rows, cols, len(Ps) + 1)
plt.plot(Ps, var_list, marker='o')
plt.title("P vs Variance")
plt.xlabel("P")
plt.ylabel("Variance")

plt.tight_layout()
plt.show()