SHELL := /bin/bash
VENV := venv
ACTIVATE_VENV := source $(VENV)/bin/activate

docker_image := image
docker_container := container

.PHONY: all
all: clean-all deploy

.PHONY: deploy
deploy: fraud_detection/model/ml_model.dill.gz | $(VENV)
	$(ACTIVATE_VENV) && bin/deploy

.PHONY: docker-image
docker-image:
	docker build -t $(docker_image) .

.PHONY: docker-run
docker-run: docker-image fraud_detection/model/ml_model.dill.gz
	docker run --rm -d -p 5000:5000 --name $(docker_container) $(docker_image)

.PHONY: docker-stop
docker-stop:
	docker container stop $(docker_container)

.PHONY: docker-shell
docker-shell:
	docker exec -it $(docker_container) bash

$(VENV): requirements.txt
	rm -rf $@
	python3 -m venv $@
	$(ACTIVATE_VENV) && pip install -r $<
	touch $@

.PHONY: model
model: fraud_detection/model/ml_model.dill.gz

fraud_detection/model/ml_model.dill.gz: fraud_detection/model/fraud_model.py | $(VENV)
	$(ACTIVATE_VENV) && python -m fraud_detection.model.fraud_model

.PHONY: clean clean-all
clean:
	rm -rf $(VENV)
	find . | grep __pycache__ | xargs rm -rf

clean-all: clean
	rm -f fraud_detection/model/ml_model.dill.gz
