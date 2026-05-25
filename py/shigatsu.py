import csv
import math
import random
from pathlib import Path

try:
    import matplotlib.pyplot as plt
except ModuleNotFoundError:
    plt = None


# -----------------------------
# 基本設定
# -----------------------------

AREA_SIZE = 1000          # エリアは 1000m x 1000m
DEFAULT_NODES = 20        # 最初の課題では端末数は20台
TOTAL_TIME = 1000         # 1000単位時間だけ動かす
SPEED = 10                # 1単位時間あたり10m進む
SOURCE_NODE = 0           # 情報を最初に持っている端末を T0 とする
RECORD_INTERVAL = 100     # 100, 200, ... の時刻で記録する
RANDOM_SEED = 1           # 毎回同じ結果にするための乱数の種

OUTPUT_DIR = Path("output_shigatsu")


# -----------------------------
# 端末の配置と移動
# -----------------------------

def distance(p1, p2):
    """2点 p1, p2 の距離を求める。p1, p2 は (x, y) の形。"""
    dx = p1[0] - p2[0]
    dy = p1[1] - p2[1]
    return math.sqrt(dx * dx + dy * dy)


def random_point():
    """1000m x 1000m のエリア内からランダムに1点を選ぶ。"""
    x = random.uniform(0, AREA_SIZE)
    y = random.uniform(0, AREA_SIZE)
    return (x, y)


def make_initial_positions(node_count, min_distance=0):
    """
    端末の初期位置を作る。

    min_distance を大きくすると、端末同士が近すぎない配置になる。
    例: min_distance=50 なら、できるだけ50m以上離して置く。
    """
    positions = []

    while len(positions) < node_count:
        candidate = random_point()

        # すでに置いた全端末との距離を調べる
        ok = True
        for p in positions:
            if distance(candidate, p) < min_distance:
                ok = False
                break

        if ok:
            positions.append(candidate)

    return positions


def move_one_step(positions, destinations):
    """
    Random Waypoint モデルで全端末を1単位時間だけ動かす。

    各端末は「目的地」に向かってまっすぐ進む。
    目的地に着いたら、新しい目的地をランダムに決める。
    """
    new_positions = []
    new_destinations = []

    for position, destination in zip(positions, destinations):
        d = distance(position, destination)

        if d <= SPEED:
            # 目的地に到着できる場合は、目的地に置いてから次の目的地を決める
            new_positions.append(destination)
            new_destinations.append(random_point())
        else:
            # 目的地の方向に SPEED m だけ進む
            ratio = SPEED / d
            x = position[0] + (destination[0] - position[0]) * ratio
            y = position[1] + (destination[1] - position[1]) * ratio
            new_positions.append((x, y))
            new_destinations.append(destination)

    return new_positions, new_destinations


# -----------------------------
# 情報伝達の判定
# -----------------------------

def in_center_region(position, region_size):
    """
    position がエリア中央の正方形領域に入っているかを判定する。

    region_size=200 なら、中央の 200m x 200m の範囲だけ通信可能にする。
    """
    if region_size is None:
        return True

    left = (AREA_SIZE - region_size) / 2
    right = (AREA_SIZE + region_size) / 2
    bottom = (AREA_SIZE - region_size) / 2
    top = (AREA_SIZE + region_size) / 2

    x, y = position
    return left <= x <= right and bottom <= y <= top


def update_information(positions, informed, communication_range,
                       spread_from_all=False, center_region_size=None):
    """
    情報を受け取る端末を更新する。

    spread_from_all=False の場合:
        T0 だけが情報を渡せる。

    spread_from_all=True の場合:
        すでに情報を持っている端末なら誰でも情報を渡せる。

    center_region_size が None でなければ、
        中央の正方形領域内にいる端末同士だけが通信できる。
    """
    node_count = len(positions)
    new_informed = informed[:]

    for sender in range(node_count):
        if not informed[sender]:
            continue

        if not spread_from_all and sender != SOURCE_NODE:
            continue

        if not in_center_region(positions[sender], center_region_size):
            continue

        for receiver in range(node_count):
            if new_informed[receiver]:
                continue

            if not in_center_region(positions[receiver], center_region_size):
                continue

            if distance(positions[sender], positions[receiver]) <= communication_range:
                new_informed[receiver] = True

    return new_informed


def simulate(node_count=DEFAULT_NODES, communication_range=100,
             spread_from_all=False, center_region_size=None,
             min_initial_distance=0):
    """
    1回分のシミュレーションを行い、時刻と受信済み端末数のリストを返す。

    戻り値の例:
        [(0, 0), (100, 3), (200, 5), ...]

    ここで受信済み端末数は、最初から情報を持っている T0 を除いた数。
    """
    positions = make_initial_positions(node_count, min_initial_distance)
    destinations = [random_point() for _ in range(node_count)]

    informed = [False] * node_count
    informed[SOURCE_NODE] = True

    records = [(0, count_received_nodes(informed))]

    for t in range(1, TOTAL_TIME + 1):
        positions, destinations = move_one_step(positions, destinations)

        informed = update_information(
            positions,
            informed,
            communication_range,
            spread_from_all=spread_from_all,
            center_region_size=center_region_size,
        )

        if t % RECORD_INTERVAL == 0:
            records.append((t, count_received_nodes(informed)))

    return records


def count_received_nodes(informed):
    """T0以外で情報を受け取った端末数を数える。"""
    count = 0
    for i, has_info in enumerate(informed):
        if i != SOURCE_NODE and has_info:
            count += 1
    return count


# -----------------------------
# 結果の保存
# -----------------------------

def save_csv(filename, records_by_label):
    """
    複数のシミュレーション結果を1つのCSVに保存する。

    records_by_label は
        {"T0のみ": [(0, 0), (100, 2), ...], "全端末が中継": [...]}
    のような辞書。
    """
    OUTPUT_DIR.mkdir(exist_ok=True)
    path = OUTPUT_DIR / filename

    labels = list(records_by_label.keys())
    times = [t for t, _ in records_by_label[labels[0]]]

    with path.open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(["time"] + labels)

        for index, t in enumerate(times):
            row = [t]
            for label in labels:
                row.append(records_by_label[label][index][1])
            writer.writerow(row)

    return path


def save_svg_line_chart(filename, title, records_by_label, y_max=None):
    """
    折れ線グラフをSVGとして保存する。

    matplotlib がなくてもグラフ画像を作れるように、
    SVGの線や文字を自分で書いている。
    """
    OUTPUT_DIR.mkdir(exist_ok=True)
    path = OUTPUT_DIR / filename

    width = 900
    height = 520
    margin_left = 80
    margin_right = 40
    margin_top = 70
    margin_bottom = 70
    plot_w = width - margin_left - margin_right
    plot_h = height - margin_top - margin_bottom

    labels = list(records_by_label.keys())
    all_times = [t for t, _ in records_by_label[labels[0]]]
    max_time = max(all_times)

    if y_max is None:
        y_max = 1
        for records in records_by_label.values():
            for _, value in records:
                y_max = max(y_max, value)

    # グラフが全部0のときでも目盛りが潰れないようにする
    y_max = max(y_max, 1)

    colors = [
        "#1f77b4", "#d62728", "#2ca02c", "#9467bd",
        "#ff7f0e", "#17becf", "#8c564b", "#e377c2",
    ]

    def x_to_pixel(t):
        return margin_left + (t / max_time) * plot_w

    def y_to_pixel(v):
        return margin_top + plot_h - (v / y_max) * plot_h

    parts = []
    parts.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}">')
    parts.append('<rect width="100%" height="100%" fill="white"/>')
    parts.append(f'<text x="{width / 2}" y="35" text-anchor="middle" font-size="22">{title}</text>')

    # 軸
    parts.append(f'<line x1="{margin_left}" y1="{margin_top}" x2="{margin_left}" y2="{margin_top + plot_h}" stroke="black"/>')
    parts.append(f'<line x1="{margin_left}" y1="{margin_top + plot_h}" x2="{margin_left + plot_w}" y2="{margin_top + plot_h}" stroke="black"/>')

    # x軸目盛り
    for t in all_times:
        x = x_to_pixel(t)
        parts.append(f'<line x1="{x:.1f}" y1="{margin_top + plot_h}" x2="{x:.1f}" y2="{margin_top + plot_h + 6}" stroke="black"/>')
        parts.append(f'<text x="{x:.1f}" y="{margin_top + plot_h + 25}" text-anchor="middle" font-size="12">{t}</text>')

    # y軸目盛り
    y_step = max(1, math.ceil(y_max / 5))
    y_tick = 0
    while y_tick <= y_max:
        y = y_to_pixel(y_tick)
        parts.append(f'<line x1="{margin_left - 6}" y1="{y:.1f}" x2="{margin_left}" y2="{y:.1f}" stroke="black"/>')
        parts.append(f'<text x="{margin_left - 12}" y="{y + 4:.1f}" text-anchor="end" font-size="12">{y_tick}</text>')
        parts.append(f'<line x1="{margin_left}" y1="{y:.1f}" x2="{margin_left + plot_w}" y2="{y:.1f}" stroke="#dddddd"/>')
        y_tick += y_step

    parts.append(f'<text x="{width / 2}" y="{height - 20}" text-anchor="middle" font-size="14">time</text>')
    parts.append(f'<text x="20" y="{height / 2}" text-anchor="middle" font-size="14" transform="rotate(-90 20 {height / 2})">received nodes except T0</text>')

    # 折れ線
    for i, label in enumerate(labels):
        color = colors[i % len(colors)]
        records = records_by_label[label]
        points = []
        for t, value in records:
            points.append(f"{x_to_pixel(t):.1f},{y_to_pixel(value):.1f}")

        parts.append(f'<polyline points="{" ".join(points)}" fill="none" stroke="{color}" stroke-width="3"/>')

        # 凡例
        legend_x = margin_left + 15
        legend_y = margin_top + 20 + i * 24
        parts.append(f'<line x1="{legend_x}" y1="{legend_y}" x2="{legend_x + 30}" y2="{legend_y}" stroke="{color}" stroke-width="3"/>')
        parts.append(f'<text x="{legend_x + 40}" y="{legend_y + 5}" font-size="14">{label}</text>')

    parts.append("</svg>")

    path.write_text("\n".join(parts), encoding="utf-8")
    return path


def save_matplotlib_line_chart(filename, title, records_by_label, y_max=None):
    """
    matplotlib が使える環境なら、PNGの折れ線グラフを保存する。

    こちらのほうが一般的なPythonのグラフ作成方法。
    ただし、matplotlib が入っていない環境でも動くように、
    この関数は matplotlib があるときだけ呼び出す。
    """
    if plt is None:
        return None

    OUTPUT_DIR.mkdir(exist_ok=True)
    path = OUTPUT_DIR / filename

    plt.figure(figsize=(9, 5))

    for label, records in records_by_label.items():
        times = [t for t, _ in records]
        values = [value for _, value in records]
        plt.plot(times, values, marker="o", label=label)

    plt.title(title)
    plt.xlabel("time")
    plt.ylabel("received nodes except T0")
    plt.grid(True)
    plt.legend()

    if y_max is not None:
        plt.ylim(0, y_max)

    plt.tight_layout()
    plt.savefig(path)
    plt.close()

    return path


def save_line_chart(file_stem, title, records_by_label, y_max=None):
    """
    グラフを保存するためのまとめ関数。

    matplotlib があれば PNG を作る。
    さらに、matplotlib がない環境でも見られるように SVG も作る。
    """
    png_path = save_matplotlib_line_chart(f"{file_stem}.png", title, records_by_label, y_max)
    svg_path = save_svg_line_chart(f"{file_stem}.svg", title, records_by_label, y_max)

    return png_path, svg_path


# -----------------------------
# 課題ごとの実験
# -----------------------------

def run_experiment_4_and_5():
    """課題4・5: T0だけが送る場合と、全端末が中継できる場合を比較する。"""
    random.seed(RANDOM_SEED)
    only_t0 = simulate(communication_range=100, spread_from_all=False, min_initial_distance=30)

    random.seed(RANDOM_SEED)
    relay = simulate(communication_range=100, spread_from_all=True, min_initial_distance=30)

    results = {
        "T0 only, range 100m": only_t0,
        "Relay allowed, range 100m": relay,
    }

    save_csv("experiment_4_5.csv", results)
    save_line_chart("experiment_4_5", "T0 only vs relay allowed", results, y_max=DEFAULT_NODES - 1)


def run_experiment_6():
    """課題6: 通信距離を 50m, 100m, 150m に変えて比較する。"""
    results = {}

    for r in [50, 100, 150]:
        random.seed(RANDOM_SEED)
        records = simulate(communication_range=r, spread_from_all=True, min_initial_distance=30)
        results[f"Relay allowed, range {r}m"] = records

    save_csv("experiment_6_range.csv", results)
    save_line_chart("experiment_6_range", "Comparison of communication range", results, y_max=DEFAULT_NODES - 1)


def run_experiment_7_region_size():
    """
    課題7の一部:
    端末数を100台に固定し、中央の通信可能領域の大きさを変える。
    """
    node_count = 100
    results = {}

    random.seed(RANDOM_SEED)
    full_area = simulate(node_count=node_count, communication_range=100, spread_from_all=True)
    results["Full area"] = full_area

    for size in [100, 200, 400, 600, 800]:
        random.seed(RANDOM_SEED)
        records = simulate(
            node_count=node_count,
            communication_range=100,
            spread_from_all=True,
            center_region_size=size,
        )
        results[f"Center {size}x{size}"] = records

    save_csv("experiment_7_region_size.csv", results)
    save_line_chart("experiment_7_region_size", "Center communication region size", results, y_max=node_count - 1)


def run_experiment_7_node_count():
    """
    課題7の一部:
    中央の通信可能領域を 400m x 400m に固定し、端末数を変える。
    """
    results = {}

    for node_count in [20, 50, 100, 150]:
        random.seed(RANDOM_SEED)
        records = simulate(
            node_count=node_count,
            communication_range=100,
            spread_from_all=True,
            center_region_size=400,
        )
        results[f"{node_count} nodes"] = records

    save_csv("experiment_7_node_count.csv", results)
    save_line_chart("experiment_7_node_count", "Comparison of node count", results, y_max=149)


def main():
    """プログラムを実行したときに呼ばれる場所。"""
    run_experiment_4_and_5()
    run_experiment_6()
    run_experiment_7_region_size()
    run_experiment_7_node_count()

    print("シミュレーションが終わりました。")
    print(f"結果は {OUTPUT_DIR} フォルダに保存しました。")
    if plt is None:
        print("このPythonでは matplotlib が見つからなかったので、SVGグラフを保存しました。")
    else:
        print("matplotlib が使えたので、PNGグラフも保存しました。")


if __name__ == "__main__":
    main()
