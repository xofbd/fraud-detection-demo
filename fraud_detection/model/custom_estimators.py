import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin


class Duration(BaseEstimator, TransformerMixin):

    def __init__(self, directive=None):
        self.directive = directive

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        start = pd.to_datetime(X.iloc[:, 1], format=self.directive)
        end = pd.to_datetime(X.iloc[:, 0], format=self.directive)

        return (end - start).dt.total_seconds().values.reshape(-1, 1)
