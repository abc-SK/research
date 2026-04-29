import random
import math
import matplotlib.pyplot as plt

SPEED = 10
N = 20
AREA = 1000
TIME = 1000

# 距離関数
def distance(a, b):
    dx = a[0] - b[0]
    dy = a[1] - b[1]
    return math.sqrt(dx*dx + dy*dy)

# 初期位置
nodes = []
for i in range(N):
    x = random.uniform(0, AREA)
    y = random.uniform(0, AREA)
    nodes.append([x, y])

# 目的地
targets = []
for i in range(N):
    tx = random.uniform(0, AREA)
    ty = random.uniform(0, AREA)
    targets.append([tx, ty])

# 情報を持っているか
received = [False] * N
received[0] = True  # T0

# --------------------------
# シミュレーション
# --------------------------

times = []
counts = []

for t in range(TIME):

    # 移動
    for i in range(N):
        x, y = nodes[i]
        tx, ty = targets[i]

        dx = tx - x
        dy = ty - y
        dist = math.sqrt(dx*dx + dy*dy)

        if dist > SPEED:
            nodes[i][0] += SPEED * dx / dist
            nodes[i][1] += SPEED * dy / dist
        else:
            nodes[i][0] = tx
            nodes[i][1] = ty

            # 新しい目的地
            targets[i] = [
                random.uniform(0, AREA),
                random.uniform(0, AREA)
            ]

    # 通信（T0のみ）
    for i in range(N):
        if distance(nodes[0], nodes[i]) <= 100:
            received[i] = True

    # 途中確認（100ごと）
    if t % 100 == 0:
        print("time:", t, "受信数:", sum(received))
    
    times.append(t)
    counts.append(sum(received))

plt.plot(times, counts)
plt.xlabel("Time")
plt.ylabel("Received Nodes")
plt.show()

#グラフ直す。点が近くならないようにする。