"""
Analyze QuantumHPC MPI scaling benchmark results.

Reads:
    results/logs/mpi_scaling.csv

Produces:
    results/logs/mpi_scaling_summary.csv
    plots/mpi_scaling/runtime_vs_processes.png
    plots/mpi_scaling/speedup_vs_processes.png
    plots/mpi_scaling/efficiency_vs_processes.png
"""

from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt


# ============================================================
# Paths
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

INPUT_FILE = (
    PROJECT_ROOT
    / "results"
    / "logs"
    / "mpi_scaling.csv"
)

OUTPUT_FILE = (
    PROJECT_ROOT
    / "results"
    / "logs"
    / "mpi_scaling_summary.csv"
)

PLOT_DIR = (
    PROJECT_ROOT
    / "plots"
    / "mpi_scaling"
)

PLOT_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================
# Load results
# ============================================================

df = pd.read_csv(INPUT_FILE)

if df.empty:
    raise ValueError("MPI scaling CSV contains no results.")

required_columns = {
    "processes",
    "samples",
    "repeats",
    "features",
    "qubits",
    "shots",
    "backend",
    "condition",
    "wall_time_ms",
    "simulation_time_ms",
}

missing_columns = required_columns - set(df.columns)

if missing_columns:
    raise ValueError(
        f"Missing required columns: {sorted(missing_columns)}"
    )


# ============================================================
# Basic experiment information
# ============================================================

print("=" * 60)
print("QuantumHPC MPI Scaling Analysis")
print("=" * 60)

print(f"Input file : {INPUT_FILE}")
print(f"Total runs : {len(df)}")

print("\nConfigurations:")
print(
    df[
        [
            "processes",
            "samples",
            "repeats",
            "features",
            "qubits",
            "shots",
            "backend",
            "condition",
        ]
    ].drop_duplicates().to_string(index=False)
)


# ============================================================
# Group results by MPI process count
# ============================================================

summary = (
    df.groupby("processes")["wall_time_ms"]
    .agg(
        trials="count",
        mean_wall_time_ms="mean",
        min_wall_time_ms="min",
        max_wall_time_ms="max",
        std_wall_time_ms="std",
    )
    .reset_index()
)


# ============================================================
# Calculate speedup and efficiency
# ============================================================

baseline = summary.loc[
    summary["processes"] == 1,
    "mean_wall_time_ms",
]

if baseline.empty:
    raise ValueError(
        "No 1-process baseline was found."
    )

baseline_time = baseline.iloc[0]

summary["speedup"] = (
    baseline_time
    / summary["mean_wall_time_ms"]
)

summary["efficiency"] = (
    summary["speedup"]
    / summary["processes"]
)

summary["efficiency_percent"] = (
    summary["efficiency"]
    * 100
)


# ============================================================
# Print summary
# ============================================================

print("\nScaling Summary")
print("=" * 60)

display_columns = [
    "processes",
    "trials",
    "mean_wall_time_ms",
    "min_wall_time_ms",
    "max_wall_time_ms",
    "std_wall_time_ms",
    "speedup",
    "efficiency_percent",
]

print(
    summary[display_columns]
    .round(3)
    .to_string(index=False)
)


# ============================================================
# Save summary CSV
# ============================================================

summary.to_csv(
    OUTPUT_FILE,
    index=False,
)

print(f"\nSummary saved to:")
print(OUTPUT_FILE)


# ============================================================
# Plot 1: Runtime vs MPI processes
# ============================================================

plt.figure(figsize=(9, 6))

plt.errorbar(
    summary["processes"],
    summary["mean_wall_time_ms"],
    yerr=summary["std_wall_time_ms"],
    marker="o",
    capsize=5,
)

plt.xlabel("MPI Processes")
plt.ylabel("Mean Wall Time (ms)")
plt.title("QuantumHPC MPI Runtime Scaling")

plt.xticks(summary["processes"])
plt.grid(True, alpha=0.3)

plt.tight_layout()

runtime_plot = (
    PLOT_DIR
    / "runtime_vs_processes.png"
)

plt.savefig(runtime_plot, dpi=300)
plt.close()

print(f"Runtime plot saved to:")
print(runtime_plot)


# ============================================================
# Plot 2: Speedup vs MPI processes
# ============================================================

plt.figure(figsize=(9, 6))

plt.plot(
    summary["processes"],
    summary["speedup"],
    marker="o",
    label="Measured speedup",
)

# Ideal linear speedup
plt.plot(
    summary["processes"],
    summary["processes"],
    linestyle="--",
    label="Ideal linear speedup",
)

plt.xlabel("MPI Processes")
plt.ylabel("Speedup")
plt.title("QuantumHPC MPI Speedup")

plt.xticks(summary["processes"])
plt.grid(True, alpha=0.3)
plt.legend()

plt.tight_layout()

speedup_plot = (
    PLOT_DIR
    / "speedup_vs_processes.png"
)

plt.savefig(speedup_plot, dpi=300)
plt.close()

print(f"Speedup plot saved to:")
print(speedup_plot)


# ============================================================
# Plot 3: Parallel efficiency
# ============================================================

plt.figure(figsize=(9, 6))

plt.plot(
    summary["processes"],
    summary["efficiency_percent"],
    marker="o",
)

plt.axhline(
    100,
    linestyle="--",
)

plt.xlabel("MPI Processes")
plt.ylabel("Parallel Efficiency (%)")
plt.title("QuantumHPC MPI Parallel Efficiency")

plt.xticks(summary["processes"])
plt.ylim(0, 110)
plt.grid(True, alpha=0.3)

plt.tight_layout()

efficiency_plot = (
    PLOT_DIR
    / "efficiency_vs_processes.png"
)

plt.savefig(efficiency_plot, dpi=300)
plt.close()

print(f"Efficiency plot saved to:")
print(efficiency_plot)


# ============================================================
# Complete
# ============================================================

print("\nAnalysis complete.")