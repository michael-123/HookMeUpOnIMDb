setup:
	mkdir data; virtualenv -p python3 venv; . venv/bin/activate; pip install -r requirements.txt; deactivate
