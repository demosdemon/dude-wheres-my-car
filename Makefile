.PHONY: clean dist-clean install build lock requirements

clean:
	git clean -xdf -e .env -e node_modules -e .venv

dist-clean:
	git clean -xdf -e .env

install: Pipfile.lock package.json
	PIPENV_VENV_IN_PROJECT=1 pipenv sync --dev
	npm install

Pipfile.lock: Pipfile
	PIPENV_VENV_IN_PROJECT=1 pipenv lock

lock: Pipfile.lock

requirements: Pipfile.lock
	pipenv lock -r > requirements/production.txt
	pipenv lock -rd > requirements/development.txt

build:
	@echo 'Not Implemented yet.'
	@false
