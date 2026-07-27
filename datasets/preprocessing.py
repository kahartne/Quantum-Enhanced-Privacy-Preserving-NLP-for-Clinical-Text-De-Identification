"""
preprocessing.py

Dataset preprocessing utilities.
"""

import numpy as np


class DataPreprocessor:

    def __init__(self, dataframe):

        self.df = dataframe

    def numeric_features(self):

        return self.df.select_dtypes(
            include=np.number
        )

    def text_features(self):

        return self.df.select_dtypes(
            exclude=np.number
        )

    def feature_matrix(self):

        return self.numeric_features().to_numpy()

    def number_of_features(self):

        return self.numeric_features().shape[1]
    
    def feature_names(self):
        """
        Return the names of numeric features.
        """

        return list(
            self.numeric_features().columns
        )