
PORT=5000
VENV_NAME=venv

create-venv:
	python3 -m venv $(VENV_NAME)
	. $(VENV_NAME)/bin/activate && pip3 install -r requirements.txt

reinstall-dependencies:
	. $(VENV_NAME)/bin/activate && pip3 install -r requirements.txt

run:
	. $(VENV_NAME)/bin/activate 
	python3 manage.py run

clean:
	find . -name '*.pyc' -delete
	find . -name '__pycache__' -delete

start-database:
	. $(VENV_NAME)/bin/activate
	python3 manage.py db init 
	python3 manage.py db migrate 
	python3 manage.py db upgrade 

test:
	. $(VENV_NAME)/bin/activate
	pytest --cov

poblate-database:
	. $(VENV_NAME)/bin/activate
	cd poblate && python3 poblate.py
activate-hot-reload:
	export FLASK_ENV=development

run-formatter:
	black .
.PHONY: venv run clean distclean
