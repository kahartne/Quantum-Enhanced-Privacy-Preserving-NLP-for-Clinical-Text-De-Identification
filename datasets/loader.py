"""
loader.py

Dataset loading utilities.
Supports multiple file formats.
"""

from pathlib import Path

import pandas as pd


class DatasetLoader:
    """
    Generic dataset loader.

    Supports:
        CSV
        TSV
        JSON
        Excel
        Parquet
    """

    def __init__(self, filepath):

        self.filepath = Path(filepath)
        self.data = None

    def load(self):

        suffix = self.filepath.suffix.lower()

        if suffix == ".csv":
            self.data = pd.read_csv(self.filepath)

        elif suffix == ".tsv":
            self.data = pd.read_csv(
                self.filepath,
                sep="\t"
            )

        elif suffix in [".xlsx", ".xls"]:
            self.data = pd.read_excel(self.filepath)

        elif suffix == ".json":
            self.data = pd.read_json(self.filepath)

        elif suffix == ".parquet":
            self.data = pd.read_parquet(self.filepath)

        else:
            raise ValueError(
                f"Unsupported dataset type: {suffix}"
            )

        return self.data

    def shape(self):
        return self.data.shape

    def columns(self):
        return list(self.data.columns)

    def preview(self, rows=5):
        return self.data.head(rows)

    def info(self):
        """
        Print a summary of the dataset.
        """
        self.data.info()

    def numeric_columns(self):
        return list(
            self.data.select_dtypes(include="number").columns
        )

    def text_columns(self):
        return list(
            self.data.select_dtypes(exclude="number").columns
        )