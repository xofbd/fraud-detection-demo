import os

from flask import Flask, render_template, request
import pandas as pd

from fraud_detection.model.fraud_model import deploy_model

app = Flask(__name__)
model_path = os.path.join('fraud_detection', 'model', 'ml_model.dill.gz')
MODEL = deploy_model(model_path)


@app.route('/', methods=['GET'])
def main():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    df = process_inputs()
    y_proba = MODEL.predict_proba(df)

    return f"Probability of fraud: {100 * y_proba[0, 1] :g} %"


def process_inputs():
    """Process submitted data for ML model."""

    # ColumnTransformer will complain if there are columns missing even if they
    # are dropped. Further, to prevent an error when predicting, the columns of
    # the DataFrame need to be in the same order as when fitting.
    inputs = dict(request.form)
    inputs.update({'user_id': 0, 'device_id': 0, 'ip_address': 0})

    return pd.DataFrame(inputs,
                        index=[0],
                        columns=['user_id', 'signup_time', 'purchase_time',
                                 'purchase_value', 'device_id', 'source',
                                 'browser', 'sex', 'age', 'ip_address'])


if __name__ == '__main__':
    app.run()
