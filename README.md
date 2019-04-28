# RASA_NLU_BASE
## Setup
```
cd [PATH TO]/RASA_NLU_BASE/
virtualenv rasa
source rasa/bin/activate


# If there are previous rasa installations , uninstall them
pip uninstall rasa_nlu --user
pip uninstall rasa_core --user
pip uninstall rasa_core_sdk --user

# install latest version of rasa nlu
pip install rasa_nlu --user
pip install rasa_nlu[spacy] --user
python3 -c "import rasa_nlu; print(rasa_nlu.__version__)"
python3 -m spacy download en_core_web_md
python3 -m spacy link en_core_web_md en

# install latest version of rasa core
pip install rasa_core
python3 -c "import rasa_core; print(rasa_core.__version__)"

# install latest version of rasa core sdk
pip install rasa_core_sdk
python3 -c "import rasa_core_sdk; print(rasa_core.__version__)"

# install other libraries
pip install beautifulsoup4
pip install pandas
pip install Flask-Mail

python dialogue_management_model.py
```
## NLU
### To train nlu model
```
python nlu_model.py
```
### To run nlu model over http
```
python App_nlu.py
```
## Core
### To train core model
```
python train_init.py
```
### To test conversation via cli
```
python dialogue_management_model.py
```
### To train core model online
```
python train_online.py
```
