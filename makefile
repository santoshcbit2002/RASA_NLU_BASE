.PHONY: clean setupbot checkbot startbot runbot

setupbot:
	pip uninstall --yes rasa_nlu 
	pip uninstall --yes rasa_core 
	pip install rasa_nlu --user
	pip install rasa_nlu[spacy] --user
	python3 -m spacy download en_core_web_md --force
	python3 -m spacy link en_core_web_md en --force
	pip install rasa_core --user
	pip uninstall --yes rasa_core_sdk 
	pip install rasa_core_sdk --user
	pip install beautifulsoup4	
	pip install pandas
	pip install Flask-Mail
	
checkbot:
	python3 -c "import rasa_nlu; print('**** Rasa NLU Version: ',rasa_nlu.__version__)"
	python3 -c "import rasa_core; print('**** Rasa Core Version: ',rasa_core.__version__)"
	python3 -c "import rasa_core_sdk; print('**** Rasa SDK Version: ',rasa_core_sdk.__version__)"

startbot:
	python3 nlu_model.py
	python3 train_init.py
	python3 -m rasa_core_sdk.endpoint --actions actions

runbot:
	python3 -m rasa_core.run --nlu models/nlu/default/restaurantnlu --core models/dialogue --endpoints endpoints.yml

trainbot:
	python3 -m rasa_core.train interactive -o models/dialogue -d restaurant_domain.yml -c policies.yml -s data/stories.md --nlu models/nlu/default/restaurantnlu --endpoints endpoints.yml
	