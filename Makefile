.PHONY: clean dist-clean install build lock

clean:
	git clean -xdf -e .env -e node_modules -e .venv

dist-clean:
	git clean -xdf -e .env

install: lock
	PIPENV_VENV_IN_PROJECT=1 pipenv sync --dev

Pipfile.lock: Pipfile
	PIPENV_VENV_IN_PROJECT=1 pipenv lock

lock: Pipfile.lock

build:
	@echo 'Not Implemented yet.'
	@false
