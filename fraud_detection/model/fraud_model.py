import gzip
import os

import dill
import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

from fraud_detection.model.custom_estimators import Duration


def create_model():
    """Return trained ML model."""
    X_train, X_test, y_train, y_test = prepare_data()

    # Columns to use for model
    cat_columns = ['source', 'browser', 'sex']
    num_columns = ['purchase_value', 'age']
    time_columns = ['purchase_time', 'signup_time']

    # Build model
    selector = ColumnTransformer([
        ('categorical', OneHotEncoder(sparse=False), cat_columns),
        ('numerical', 'passthrough', num_columns),
        ('time', Duration(directive='%Y-%m-%d %H:%M:%S'), time_columns)],
        remainder='drop')
    clf = RandomForestClassifier(n_estimators=50, random_state=0)
    model = Pipeline([('selector', selector),
                      ('classifier', clf)])

    # Tune model hyperparameters
    param_grid = {'classifier__max_depth': range(2, 20),
                  'classifier__class_weight': ['balanced', None]}
    grid_search = GridSearchCV(model, param_grid,
                               cv=5,
                               n_jobs=2,
                               verbose=1,
                               scoring=cost_function)

    return grid_search.fit(X_train, y_train)


def prepare_data():
    """Return training and testing data sets."""
    file_path = os.path.join('data', 'Fraud_Data.csv')
    df = pd.read_csv(file_path)
    X = df.drop('class', axis=1)
    y = df['class']

    return train_test_split(X, y, test_size=0.2, random_state=0)


def cost_function(model, X, y_true):
    """
    Return cost (as negative) based on false positives and false negatives.

    If we fail to identify an instance of fraud (positive class), we get
    penalized by the amount of the transaction. If we identify a legitimate
    transaction as fraud, we incur a flat $8 penalty.
    """
    false_pos_rate = 8

    y_pred = model.predict(X)
    ind_false_pos = (y_pred != y_true) & (y_pred == 1)
    ind_false_neg = (y_pred != y_true) & (y_pred == 0)

    false_neg_cost = X.loc[ind_false_neg, 'purchase_value'].sum()
    false_pos_cost = false_pos_rate * ind_false_pos.sum()

    return -(false_neg_cost + false_pos_cost)


def preserve_model(model, path_name=None):
    """Preserve ML model to disk using dill."""
    if path_name is None:
        path_name = os.path.join('fraud_detection', 'model',
                                 'ml_model.dill.gz')
    with gzip.open(path_name, 'wb') as f:
        dill.dump(model, f)


def deploy_model(model_path):
    """Return loaded ML model from disk."""
    with gzip.open(model_path, 'rb') as f:
        return dill.load(f)


if __name__ == '__main__':
    model = create_model()
    preserve_model(model)
