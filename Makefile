SHELL := /bin/bash

.PHONY: all deploy model clean remove_all

all: clean_all venv fraud_detection/model/ml_model.dill.gz deploy

deploy: venv fraud_detection/model/ml_model.dill.gz
	source venv/bin/activate && \
	export FLASK_APP="fraud_detection/flask_app/app.py" && \
	export FLASK_ENV=development && \
	export FLASK_DEBUG=true && \
	python -m flask run

venv: requirements.txt
	test -d venv || python3 -m venv venv
	source venv/bin/activate && \
	pip install -r requirements.txt
	touch venv

fraud_detection/model/ml_model.dill.gz: venv fraud_detection/model/fraud_model.py
	source venv/bin/activate && \
	python -m fraud_detection.model.fraud_model

model: fraud_detection/model/ml_model.dill.gz

clean:
	rm -rf venv
	find . | grep __pycache__ | xargs rm -rf

clean_all: clean
	rm -f fraud_detection/model/ml_model.dill.gz
