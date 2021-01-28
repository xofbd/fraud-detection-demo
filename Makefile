SHELL := /bin/bash
ACTIVATE_VENV := source venv/bin/activate

.PHONY: all
all: clean-all deploy

.PHONY: deploy deploy-docker docker-rm
deploy: fraud_detection/model/ml_model.dill.gz | venv
	$(ACTIVATE_VENV) && bin/deploy

deploy-docker: fraud_detection/model/ml_model.dill.gz docker-rm
	docker build -t fraud_detection .
	docker run -d -p 5000:5000 flask_app fraud_detection

docker-rm:
	-docker rm -f flask_app

venv: requirements.txt
	test -d $@ || python3 -m venv $@
	$(ACTIVATE_VENV) && pip install -r $<
	touch $@

.PHONY: model
model: fraud_detection/model/ml_model.dill.gz

fraud_detection/model/ml_model.dill.gz: fraud_detection/model/fraud_model.py | venv
	$(ACTIVATE_VENV) && python -m fraud_detection.model.fraud_model

.PHONY: clean clean-all
clean:
	rm -rf venv
	find . | grep __pycache__ | xargs rm -rf

clean-all: clean
	rm -f fraud_detection/model/ml_model.dill.gz
