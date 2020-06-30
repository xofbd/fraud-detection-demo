import numpy as np
import scipy

from predict_fraud import cost_function, prepare_data


def scoring_function(threshold, model, X, y_true):
    y_pred = np.zeros_like(y_true)
    y_proba = model.predict_proba(X)[:, 1]
    ind_pos = y_proba > threshold
    y_pred[ind_pos] = 1

    false_pos_rate = 8

    ind_false_pos = (y_pred != y_true) & (y_pred == 1)
    ind_false_neg = (y_pred != y_true) & (y_pred == 0)

    false_neg_cost = X.loc[ind_false_neg, 'purchase_value'].sum()
    false_pos_cost = false_pos_rate * ind_false_pos.sum()

    print(f"Number of False Positives: {ind_false_pos.sum()}")
    print(f"Number of False Negatives: {ind_false_neg.sum()}")

    return false_neg_cost + false_pos_cost


def optimize_threshold(model, X, y_true):
    output = scipy.optimize.minimize_scalar(scoring_function,
                                            args=(model, X, y_true),
                                            bounds=(0.01, 0.99),
                                            method='Bounded')
    return output


if __name__ == '__main__':
    import os

    import joblib

    X_train, X_test, y_train, y_test = prepare_data()

    model = joblib.load(os.path.join('model', 'model.joblib'))
    output = optimize_threshold(model, X_train, y_train)
