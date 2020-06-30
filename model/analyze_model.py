import os

import joblib
import matplotlib.pyplot as plt
from sklearn.metrics import plot_precision_recall_curve

from predict_fraud import prepare_data


def plot_cost_vs_threshold():
    pass


if __name__ == '__main__':
    _, X_test, _, y_test = prepare_data()
    model = joblib.load(os.path.join('model', 'model.joblib'))

    plot_precision_recall_curve(model, X_test, y_test)
    plt.show()
