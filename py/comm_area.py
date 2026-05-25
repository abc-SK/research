import random
import math
import copy
import matplotlib.pyplot as plt

# --------------------------
# パラメータ
# --------------------------
SPEED = 10
N = 20
AREA = 1000
TIME = 1000
MINIMUM_DISTANCE = 60


# 比較する通信半径
RANGES = [50, 100, 150]

# --------------------------
# 距離関数
# --------------------------
def distance(a, b):

    dx = a[0] - b[0]
    dy = a[1] - b[1]

    return math.sqrt(dx*dx + dy*dy)

# --------------------------
# 最小距離チェック
# --------------------------
def is_far_enough(new_point, points, min_dist):

    for p in points:

        if distance(new_point, p) < min_dist:
            return False

    return True

# --------------------------
# 点生成
# --------------------------
def generate_points(n, area, min_dist, max_attempts=10000):

    points = []
    attempts = 0

    while len(points) < n and attempts < max_attempts:

        new_point = [
            random.uniform(0, area),
            random.uniform(0, area)
        ]

        if is_far_enough(new_point, points, min_dist):
            points.append(new_point)

        attempts += 1

    return points

# --------------------------
# シミュレーション
# spread=False : T0のみ
# spread=True  : 受信端末も送信
# --------------------------
def simulate(initial_nodes,
             initial_targets,
             communication_range,
             spread):

    nodes = copy.deepcopy(initial_nodes)
    targets = copy.deepcopy(initial_targets)

    received = [False] * N
    received[0] = True

    times = []
    counts = []

    for t in range(TIME):

        # --------------------------
        # 移動
        # --------------------------
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

                nodes[i] = [tx, ty]

                # 新しい目的地
                while True:

                    new_target = [
                        random.uniform(0, AREA),
                        random.uniform(0, AREA)
                    ]

                    if is_far_enough(
                        new_target,
                        targets,
                        MINIMUM_DISTANCE
                    ):

                        targets[i] = new_target
                        break

        # --------------------------
        # 通信
        # --------------------------

        if spread == False:

            # T0のみ送信
            for i in range(N):

                if distance(nodes[0], nodes[i]) <= communication_range:
                    received[i] = True

        else:

            # 受信済み端末も送信
            new_received = received.copy()

            for i in range(N):

                if received[i]:

                    for j in range(N):

                        if distance(nodes[i], nodes[j]) <= communication_range:
                            new_received[j] = True

            received = new_received

        # --------------------------
        # 100刻みで保存
        # --------------------------
        if t % 100 == 0:

            times.append(t)
            counts.append(sum(received))

    return times, counts

# --------------------------
# 初期条件
# --------------------------
initial_nodes = generate_points(
    N,
    AREA,
    MINIMUM_DISTANCE
)

initial_targets = generate_points(
    N,
    AREA,
    MINIMUM_DISTANCE
)

# --------------------------
# 実験
# --------------------------
results = {}

for r in RANGES:

    # T0のみ
    times1, counts1 = simulate(
        initial_nodes,
        initial_targets,
        communication_range=r,
        spread=False
    )

    # 拡散あり
    times2, counts2 = simulate(
        initial_nodes,
        initial_targets,
        communication_range=r,
        spread=True
    )

    results[(r, False)] = (times1, counts1)
    results[(r, True)] = (times2, counts2)

# --------------------------
# グラフ
# --------------------------
for r in RANGES:

    # T0のみ
    times, counts = results[(r, False)]

    plt.plot(
        times,
        counts,
        marker="o",
        label=f"{r}m : T0 only"
    )

    # 拡散あり
    times, counts = results[(r, True)]

    plt.plot(
        times,
        counts,
        marker="s",
        linestyle="--",
        label=f"{r}m : Spread"
    )

plt.xlabel("Time")
plt.ylabel("Received Nodes")

plt.yticks(range(0, N + 1))
plt.ylim(0, N + 1)

plt.grid(True)
plt.legend()

plt.show()