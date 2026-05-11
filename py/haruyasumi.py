import random
import matplotlib.pyplot as plt

N = 10
TRIALS = 100

Ps = [0.1, 0.3, 0.5, 0.7, 0.9]

for P in Ps:
    results = []

    # グラフ生成
    edges = []
    for i in range(N):
        for j in range(i+1, N):
            if random.random() < P:
                edges.append((i, j))

    adj = [[0]*N for _ in range(N)]
    for a, b in edges:
        adj[a][b] = 1
        adj[b][a] = 1

    # 彩色
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

    # シミュレーション
    for _ in range(TRIALS):
        order = list(range(N))
        random.shuffle(order)
        results.append(greedy_coloring(order))

    # --------------------------
    # ヒストグラム表示
    # --------------------------
    plt.figure()
    plt.hist(results, bins=range(min(results), max(results)+2), edgecolor='black')
    plt.title(f"P = {P}")
    plt.xlabel("Number of colors")
    plt.ylabel("Frequency")
    plt.grid()

    plt.show()