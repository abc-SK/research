from utils import generate_points

for d in [60, 55, 50, 45, 40, 35, 30]:
    ok = 0
    trials = 20
    for _ in range(trials):
        pts = generate_points(200, 1000, d, max_attempts=50000)
        if len(pts) == 200:
            ok += 1
    print(f"{d}: {ok}/{trials}")
