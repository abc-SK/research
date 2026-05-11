import random

N = 10
TRIALS = 100
Ps=[0.1,0.3,0.5,0.7,0.9]



for P in Ps:
    results = []

#グラフ生成
edges = []

for i in range(N):
    for j in range(i+1, N):
        if random.random() < P:
            edges.append((i, j))

adj = [[0]*N for _ in range(N)]

for a, b in edges:
    adj[a][b] = 1
    adj[b][a] = 1

print("Edges:")
print(edges)

# --------------------------
# 貪欲彩色（色配列も返す）
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

    return color, max(color)

# --------------------------
# 1回分（手で確認用）
# --------------------------
order = list(range(N))
random.shuffle(order)

color, num_colors = greedy_coloring(order)

print("\n=== Sample ===")
print("Order:")
print(order)

print("\nColor (index = vertex):")
print(color)

print("\nNumber of colors:", num_colors)

# --------------------------
# 100回シミュレーション
# --------------------------
results = []

for _ in range(TRIALS):
    order = list(range(N))
    random.shuffle(order)
    _, num = greedy_coloring(order)
    results.append(num)

#分散計算
avg = sum(results)/TRIALS
var = sum((x - avg) ** 2 for x in results) / TRIAL

print("\n=== Results ===")
print(results)
print("min =", min(results))
print("max =", max(results))
print("avg =", sum(results)/TRIALS)
