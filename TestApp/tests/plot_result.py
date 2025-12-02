import pandas as pd
import matplotlib.pyplot as plt
import os

RESULTS_CSV = os.path.join(os.path.dirname(__file__), "..", "results", "benchmark_results.csv")


def plot_last_run():
    df = pd.read_csv(RESULTS_CSV)
    if df.empty:
        print("No data available to display graphs")
        return

    df['avg_s'] = df['avg_ms'] / 1000.0

    last_run_id = df['run_id'].max()
    df_last = df[df['run_id'] == last_run_id]

    records_count = df_last['records'].unique()
    records_label = f"Records tested: {records_count[0]}" if len(
        records_count) == 1 else f"Records tested: {records_count}"

    df_last['label'] = df_last.apply(
        lambda row: (
            "mongo6" if row['container_name'] == "mongo6_db" else
            "mongo8" if row['container_name'] == "mongo8_db" else
            row['db_type']
        ),
        axis=1
    )

    operations = ['insert', 'select', 'update', 'delete']

    colors = {
        'postgresql': 'blue',
        'mysql': 'orange',
        'mongo': 'gray',
        'mongo6': 'gray',
        'mongo8': 'gray'
    }

    fig, axes = plt.subplots(1, 4, figsize=(20, 5))

    for i, op in enumerate(operations):
        ax = axes[i]
        df_op = df_last[df_last['operation'] == op]

        if df_op.empty:
            ax.set_title(op.upper())
            continue

        bases = df_op['label'].unique()
        means = [df_op[df_op['label'] == b]['avg_s'].mean() for b in bases]

        colors_list = [colors.get(b, 'gray') for b in bases]

        bars = ax.bar(bases, means, color=colors_list)
        ax.set_title(op.upper())
        ax.set_ylabel("Time [s]")
        ax.set_xlabel("Database")
        ax.grid(axis='y', linestyle='--', alpha=0.7)

        if means:
            max_height = max(means)

            limit_buffer = max_height * 0.15 if max_height > 0 else 1.0
            ax.set_ylim(0, max_height + limit_buffer)

            offset = max_height * 0.01
        else:
            offset = 0.01

        for j, v in enumerate(means):
            text_label = f"{v:.4f}s" if v < 0.01 else f"{v:.2f}s"

            ax.text(
                j,
                v + offset,
                text_label,
                ha='center',
                va='bottom',
                fontsize=9,
                fontweight='bold'
            )
        # -----------------------------

    fig.suptitle(f"{records_label}", fontsize=14, y=1)

    plt.tight_layout()
    plt.show()