SHELL := /bin/bash

.PHONY: all clean deploy model update_model remove_venv remove_model

all: venv model/ml_model.dill.gz

deploy: venv model/ml_model.dill.gz
	source venv/bin/activate && export FLASK_APP=app.py && python -m flask run

venv:
	python3 -m venv venv
	source venv/bin/activate && pip install -r requirements.txt

model/ml_model.dill.gz: venv
	source venv/bin/activate && python -m model.fraud_model

model: venv model/ml_model.dill.gz

update_model: venv remove_model model/ml_model.dill.gz

clean: remove_venv remove_model

remove_venv:
	rm -rf venv

remove_model:
	rm model/ml_model.dill.gz
