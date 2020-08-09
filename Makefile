SHELL := /bin/bash

.PHONY: all deploy model update_model clean remove_venv remove_model

all: venv fraud_detection/model/ml_model.dill.gz deploy

deploy: venv fraud_detection/model/ml_model.dill.gz
	source venv/bin/activate && \
	export FLASK_APP="fraud_detection/flask_app/app.py" && \
	python -m flask run

venv: requirements.txt
	python3 -m venv venv
	source venv/bin/activate && \
	pip install -r requirements.txt

fraud_detection/model/ml_model.dill.gz: venv
	source venv/bin/activate && \
	python -m fraud_detection.model.fraud_model

model: venv fraud_detection/model/ml_model.dill.gz

update_model: venv remove_model fraud_detection/model/ml_model.dill.gz

clean: remove_venv remove_model

remove_venv:
	rm -rf venv

remove_model:
	rm -f fraud_detection/model/ml_model.dill.gz
