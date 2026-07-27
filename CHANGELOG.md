# Changelog

## Phase 1 — Project Framework

### Added

- Modular project structure
- DatasetLoader supporting CSV, TSV, Excel, JSON, and Parquet
- DataPreprocessor for numeric feature extraction
- FeatureMapBuilder using Qiskit's ZZFeatureMap
- Manual ZZFeatureMap implementation using primitive quantum gates
- ExperimentLogger with CSV output
- Runtime benchmarking
- Automatic circuit PNG generation
- Clinical sample dataset
- Clinical notes sample dataset

### Improved

- Automatic numeric feature detection
- Dynamic qubit count based on dataset features
- Organized plots and results directories
- Manual vs. library circuit comparison