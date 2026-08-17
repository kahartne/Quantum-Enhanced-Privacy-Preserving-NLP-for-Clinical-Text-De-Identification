from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt


# ------------------------------------------------------------
# Paths
# ------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]
RESULTS_DIR = PROJECT_ROOT / "results" / "logs"
PLOTS_DIR = PROJECT_ROOT / "plots" / "parameter_sweep"

PLOTS_DIR.mkdir(parents=True, exist_ok=True)


# ------------------------------------------------------------
# Load Bridges-2 parameter sweep results
# ------------------------------------------------------------

result_files = sorted(RESULTS_DIR.glob("slurm-43724086_*.csv"))

if len(result_files) != 12:
    raise RuntimeError(
        f"Expected 12 parameter-sweep files, found {len(result_files)}"
    )

frames = []

for file in result_files:
    df = pd.read_csv(file)
    frames.append(df)

results = pd.concat(frames, ignore_index=True)


# ------------------------------------------------------------
# Clean / organize results
# ------------------------------------------------------------

results["Epsilon"] = results["Epsilon"].astype(float)
results["Simulation_ms"] = results["Simulation_ms"].astype(float)

results = results.sort_values(
    ["Epsilon", "Condition"]
).reset_index(drop=True)


# ------------------------------------------------------------
# Print results
# ------------------------------------------------------------

print("\nBridges-2 Parameter Sweep Results")
print("=" * 70)

print(
    results[
        ["Epsilon", "Condition", "Backend", "Qubits",
         "Features", "Shots", "Simulation_ms"]
    ].to_string(index=False)
)


# ------------------------------------------------------------
# Summary by epsilon and condition
# ------------------------------------------------------------

summary = (
    results
    .groupby(["Epsilon", "Condition"], as_index=False)["Simulation_ms"]
    .mean()
)

print("\nSummary")
print("=" * 70)
print(summary.to_string(index=False))


# ------------------------------------------------------------
# Plot: Simulation time vs epsilon
# ------------------------------------------------------------

plt.figure(figsize=(9, 6))

for condition in summary["Condition"].unique():
    condition_data = summary[
        summary["Condition"] == condition
    ]

    plt.plot(
        condition_data["Epsilon"],
        condition_data["Simulation_ms"],
        marker="o",
        label=condition,
    )

plt.xlabel("Epsilon")
plt.ylabel("Simulation Time (ms)")
plt.title("Bridges-2 CPU Simulation Time vs Epsilon")
plt.xticks([1, 2, 4, 8])
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()

plot_path = PLOTS_DIR / "simulation_time_vs_epsilon.png"
plt.savefig(plot_path, dpi=300)
plt.close()

print(f"\nPlot saved to:")
print(plot_path)


# ------------------------------------------------------------
# Save combined results
# ------------------------------------------------------------

combined_path = RESULTS_DIR / "parameter_sweep_combined.csv"

results.to_csv(combined_path, index=False)

print("\nCombined results saved to:")
print(combined_path)

# ------------------------------------------------------------
# Plot: Simulation time by condition
# ------------------------------------------------------------

pivot = summary.pivot(
    index="Epsilon",
    columns="Condition",
    values="Simulation_ms",
)

ax = pivot.plot(
    kind="bar",
    figsize=(10, 6),
)

ax.set_xlabel("Epsilon")
ax.set_ylabel("Simulation Time (ms)")
ax.set_title("Bridges-2 CPU Simulation Time by Noise Condition")
ax.legend(title="Condition")
ax.grid(axis="y", alpha=0.3)

plt.tight_layout()

bar_plot_path = PLOTS_DIR / "simulation_time_by_condition.png"
plt.savefig(bar_plot_path, dpi=300)
plt.close()

print(f"\nGrouped bar plot saved to:")
print(bar_plot_path)


# ------------------------------------------------------------
# Summary statistics by condition
# ------------------------------------------------------------

condition_stats = (
    results
    .groupby("Condition")["Simulation_ms"]
    .agg(["min", "max", "mean"])
    .reset_index()
)

condition_stats = condition_stats.rename(
    columns={
        "min": "Minimum_ms",
        "max": "Maximum_ms",
        "mean": "Average_ms",
    }
)

print("\nRuntime Statistics by Condition")
print("=" * 70)
print(condition_stats.to_string(index=False))

stats_path = RESULTS_DIR / "parameter_sweep_statistics.csv"
condition_stats.to_csv(stats_path, index=False)

print("\nStatistics saved to:")
print(stats_path)

print("\nAnalysis complete.")