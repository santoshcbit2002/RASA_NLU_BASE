.PHONY: clean train-nlu train-core cmdline server

TEST_PATH=./

train-nlu:
	python nlu_model.py

start-nlu-app:
	python App_nlu.py

train-core:
	python train_init.py

action-server:
	python -m rasa_core_sdk.endpoint --actions actions

train-online:
	make action-server&
	python -m rasa_core.train interactive -o models/dialogue -d restaurant_domain.yml -c policies.yml -s data/stories.md --nlu models/nlu/default/restaurantnlu --endpoints endpoints.yml
