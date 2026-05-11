import random
import matplotlib.pyplot as plt

N = 10
TRIALS = 100

# 比較する確率
Ps = [0.1, 0.3, 0.5, 0.7, 0.9]

avg_list = []
var_list = []

for P in Ps:
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
# グラフ描画
# --------------------------
plt.plot(Ps, var_list, marker='o')
plt.xlabel("Edge Probability P")
plt.ylabel("Variance of Colors")
plt.title("P vs Variance")
plt.grid()

plt.show()