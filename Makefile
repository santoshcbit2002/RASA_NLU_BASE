.PHONY: clean train-nlu train-core cmdline server

TEST_PATH=./

train-nlu:
	python nlu_model.py

start-nlu-app:
	python App_nlu.py

train-core:
	python train_init.py

run-simple-server:
	python -m rasa_core.run --enable_api -d models/current/dialogue -u models/current/nlu -o out.log --endpoints endpoints.yml

cmdline:
	python -m rasa_core.run -d models/current/dialogue -u models/current/nlu --endpoints endpoints.yml
	
action-server:
	python -m rasa_core_sdk.endpoint --actions actions