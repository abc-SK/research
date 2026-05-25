import random
import math
import copy

# --------------------------
# パラメータ
# --------------------------
SPEED = 10
TIME = 1000
MINIMUM_DISTANCE = 50
DEFAULT_TRIALS = 20

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
# 点の生成（最小距離あり）
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
    
    if len(points) < n:
        raise ValueError(
            f"Could not place {n} points in area {area} with min_dist={min_dist}. "
            "Please reduce MINIMUM_DISTANCE or increase the area."
        )

    return points

# --------------------------
# 複数回実行した結果の平均
# --------------------------
def average_series(series_list):
    return [
        sum(values) / len(values)
        for values in zip(*series_list)
    ]

def run_repeated_simulation(simulation_func, n, area, trials=DEFAULT_TRIALS,
                            seed_start=0, **simulation_kwargs):
    """
    同じ条件のシミュレーションを複数回実行し、時刻ごとの平均受信数を返す。
    seed_startを同じにすると、条件間で初期配置と移動乱数をそろえて比較できる。
    """
    all_counts = []
    times = None

    for trial in range(trials):
        placement_seed = seed_start + trial
        movement_seed = seed_start + 100000 + trial

        random.seed(placement_seed)
        nodes = generate_points(n, area, MINIMUM_DISTANCE)
        targets = generate_points(n, area, MINIMUM_DISTANCE)

        random.seed(movement_seed)
        trial_times, trial_counts = simulation_func(
            nodes, targets, n, area, **simulation_kwargs
        )

        if times is None:
            times = trial_times
        all_counts.append(trial_counts)

    return times, average_series(all_counts)

# --------------------------
# シミュレーション関数
# --------------------------
def simulate_communication(nodes, targets, n, area, spread=False, communication_range=100):
    """
    spread=False: T0のみ送信
    spread=True: 受信したノードも送信
    """
    nodes = copy.deepcopy(nodes)
    targets = copy.deepcopy(targets)
    
    received = [False] * n
    received[0] = True
    
    times = []
    counts = []
    
    for t in range(TIME):
        # 移動
        for i in range(n):
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

                # 新しいターゲット（最小距離制約）
                while True:
                    new_target = [
                        random.uniform(0, area),
                        random.uniform(0, area)
                    ]
                    if is_far_enough(new_target, targets, MINIMUM_DISTANCE):
                        targets[i] = new_target
                        break

        # 通信
        if spread == False:
            # T0のみ送信
            for i in range(n):
                if distance(nodes[0], nodes[i]) <= communication_range:
                    received[i] = True
        else:
            # 受信したノードも送信
            new_received = received.copy()
            for i in range(n):
                if received[i]:
                    for j in range(n):
                        if distance(nodes[i], nodes[j]) <= communication_range:
                            new_received[j] = True
            received = new_received

        # 100ステップごとに記録
        current_time = t + 1
        if current_time % 100 == 0:
            times.append(current_time)
            counts.append(sum(received))
    
    return times, counts

# --------------------------
# 限定領域通信判定
# --------------------------
def is_in_limited_area(node, center_x, center_y, area_size):
    """
    ノードが限定通信領域内にいるか確認
    center_x, center_y: 限定領域の中心
    area_size: 正方形領域の半辺長（例：100×100領域なら50）
    """
    x, y = node
    return (center_x - area_size <= x <= center_x + area_size and
            center_y - area_size <= y <= center_y + area_size)

# --------------------------
# 限定領域通信のシミュレーション関数
# --------------------------
def simulate_communication_limited_area(nodes, targets, n, area, spread=False, 
                                       communication_range=100, area_size=None):
    """
    中央の限定通信領域でシミュレーション
    area_size: 正方形領域の半辺長（Noneなら全体領域）
    """
    nodes = copy.deepcopy(nodes)
    targets = copy.deepcopy(targets)
    
    received = [False] * n
    received[0] = True
    
    times = []
    counts = []
    
    center_x = area / 2
    center_y = area / 2
    
    for t in range(TIME):
        # 移動
        for i in range(n):
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

                # 新しいターゲット（最小距離制約）
                while True:
                    new_target = [
                        random.uniform(0, area),
                        random.uniform(0, area)
                    ]
                    if is_far_enough(new_target, targets, MINIMUM_DISTANCE):
                        targets[i] = new_target
                        break

        # 通信（限定領域内のみ）
        if spread == False:
            # T0のみ送信
            for i in range(n):
                node_in_area = (area_size is None or 
                               is_in_limited_area(nodes[i], center_x, center_y, area_size))
                t0_in_area = (area_size is None or 
                             is_in_limited_area(nodes[0], center_x, center_y, area_size))
                
                if (node_in_area and t0_in_area and 
                    distance(nodes[0], nodes[i]) <= communication_range):
                    received[i] = True
        else:
            # 受信したノードも送信
            new_received = received.copy()
            for i in range(n):
                if received[i]:
                    i_in_area = (area_size is None or 
                                is_in_limited_area(nodes[i], center_x, center_y, area_size))
                    
                    for j in range(n):
                        j_in_area = (area_size is None or 
                                    is_in_limited_area(nodes[j], center_x, center_y, area_size))
                        
                        if (i_in_area and j_in_area and 
                            distance(nodes[i], nodes[j]) <= communication_range):
                            new_received[j] = True
            received = new_received

        # 100ステップごとに記録
        current_time = t + 1
        if current_time % 100 == 0:
            times.append(current_time)
            counts.append(sum(received))
    
    return times, counts
