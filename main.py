"""
Quantum HPC

Main entry point for the QuantumHPC framework.
"""

import argparse
from config import DEFAULT_CONDITION, DEFAULT_EPSILON, NOISE_CONDITIONS
from experiment.experiment_config import ExperimentConfig
from experiment.experiment_runner import ExperimentRunner


def parse_arguments():

    parser = argparse.ArgumentParser(
        description="Run a QuantumHPC experiment."
    )

    parser.add_argument(
        "--epsilon",
        type=float,
        default=DEFAULT_EPSILON,
        help="Differential privacy epsilon value."
    )

    parser.add_argument(
        "--condition",
        type=str,
        default=DEFAULT_CONDITION,
        choices=NOISE_CONDITIONS,
        help="Quantum simulation noise condition."
    )

    return parser.parse_args()


def main():

    args = parse_arguments()

    experiment_config = ExperimentConfig(
        epsilon=args.epsilon,
        condition=args.condition,
    )

    runner = ExperimentRunner(
        experiment_config
    )

    runner.run()


if __name__ == "__main__":
    main()