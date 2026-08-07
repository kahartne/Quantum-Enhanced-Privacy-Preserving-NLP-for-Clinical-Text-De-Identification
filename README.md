# QuantumHPC

Distributed Research Experience for Undergraduates (DREU) research project investigating scalable quantum simulation, high-performance computing (HPC), and quantum machine learning workflows for clinical text deidentification.

---

# Overview

QuantumHPC is a collaborative research project exploring how quantum computing and HPC technologies can be combined to support scalable quantum machine learning research.

The project focuses on:

- Manual quantum circuit construction using Qiskit
- Quantum circuit simulation with Qiskit Aer
- High-performance benchmarking
- Distributed execution using MPI
- Performance evaluation across HPC resources such as Jetstream2 and Bridges-2
- Future applications in clinical text deidentification
- [To be updated with Edmund & Sofia work]

---

# Research Objectives

The primary objectives of this project are to:

- Develop manually constructed parameterized quantum circuits without relying on high-level feature map libraries.
- Benchmark quantum simulations across CPU and GPU architectures.
- Investigate distributed quantum simulation using MPI.
- Evaluate scalability on HPC systems.
- Build a reproducible research workflow through version control and documentation.
- [To be updated with Edmund & Sofia work]

---

# Repository Structure (to be updated)

```
QuantumHPC/
│
├── backends/           Backend configuration
├── benchmark/          Performance benchmarking
├── circuits/           Quantum circuit implementations
├── data/               Sample data
├── datasets/           Dataset utilities
├── docs/               Research documentation
├── logs/               Weekly DREU research logs
├── mpi/                MPI development
├── plots/              Generated figures
├── results/            Benchmark results
├── simulation/         Quantum simulation
│
├── main.py
├── config.py
├── requirements.txt
├── TEAM_SETUP.md
├── CONTRIBUTING.md
└── CHANGELOG.md
```

---

# Current Progress (to be updated)

Completed

- Project repository established
- Manual ZZFeatureMap implementation
- Qiskit Aer simulation framework
- Initial benchmarking framework
- Team collaboration workflow
- Weekly research log
- GitHub project management

Current Work

- MPI research
- Literature review
- HPC benchmarking
- Jetstream2 deployment

Future Work

- Distributed quantum simulation
- Bridges-2 benchmarking
- Clinical dataset integration
- Quantum machine learning experiments

---

# Installation

Clone the repository

```bash
git clone https://github.com/kahartne/QuantumHPC.git
```

Create a virtual environment

```bash
python -m venv .venv
```

Activate

Windows

```bash
.venv\Scripts\activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run

```bash
python main.py
```

---

# Team

| Member | Responsibilities |
|----------|-----------------|
| Kyle Hartness | HPC, Benchmarking, MPI, Scalability, Repository Maintenance |
| Edmund Bombardieri | Quantum Circuits, Quantum Algorithms, QPE, QFI, Noise Experimentation |
| Sofia Furda | Clinical Data, Preprocessing, NLP Pipeline, Privacy-Utility |

---

# Weekly Research Log

Weekly research updates are available in the `logs/` directory.

Each weekly entry contains:

- Goals
- Approach & Implementation
- Results
- Next Steps
- References

---

# Documentation

- TEAM_SETUP.md
- CONTRIBUTING.md
- CHANGELOG.md
- ROADMAP.md

---

# Technologies (to be updated)

- Python
- Qiskit
- Qiskit Aer
- MPI (in development)
- Git
- GitHub

---

# Acknowledgements

This work is supported through the Distributed Research Experiences for Undergraduates (DREU) Program.

Research performed in collaboration with the project mentor and research team.
