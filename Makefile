.PHONY: clean dist-clean install build

clean:
	git clean -xdf -e .env -e node_modules -e .venv

dist-clean:
	git clean -xdf -e .env

install: Pipfile.lock package.json
	PIPENV_VENV_IN_PROJECT=1 pipenv sync --dev
	npm install

Pipfile.lock:
	PIPENV_VENV_IN_PROJECT=1 pipenv lock
	pipenv lock -r r

build:
	@echo 'Not Implemented yet.'
	@false
