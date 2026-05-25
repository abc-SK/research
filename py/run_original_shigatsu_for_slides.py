import contextlib
import io
import runpy
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


OUT_DIR = Path("output_shigatsu")
OUT_DIR.mkdir(exist_ok=True)

FIGURE_NAMES = [
    "original_average_non_comm_area.png",
    "original_average_limited_area_exp1.png",
    "original_average_area_size_exp2.png",
    "original_average_node_count_exp3.png",
]

figure_index = 0


def save_current_figures():
    global figure_index
    for fig_num in plt.get_fignums():
        fig = plt.figure(fig_num)
        if figure_index < len(FIGURE_NAMES):
            path = OUT_DIR / FIGURE_NAMES[figure_index]
        else:
            path = OUT_DIR / f"original_average_extra_{figure_index + 1}.png"
        fig.savefig(path, dpi=160, bbox_inches="tight")
        print(f"[saved figure] {path}")
        figure_index += 1
    plt.close("all")


def main():
    log = io.StringIO()
    original_show = plt.show
    plt.show = save_current_figures
    try:
        with contextlib.redirect_stdout(log):
            print("=== non_comm_area.py ===")
            runpy.run_path("non_comm_area.py", run_name="__main__")
            print("\n=== experiment_limited_area.py ===")
            runpy.run_path("experiment_limited_area.py", run_name="__main__")
    finally:
        plt.show = original_show

    log_text = log.getvalue()
    (OUT_DIR / "original_average_run_log.txt").write_text(log_text, encoding="utf-8")
    print(log_text)
    print(f"[saved log] {OUT_DIR / 'original_average_run_log.txt'}")


if __name__ == "__main__":
    main()
