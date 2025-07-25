default:
	@just --list

install:
	poetry install
	poetry run pre-commit install

test *flags:
	poetry run pytest --cov=stacklet {{ flags }}

pkg-prep bump="--bump-patch":
	poetry run python scripts/upgrade.py upgrade {{bump}}
	poetry update
	poetry lock
	git add justfile pyproject.toml poetry.lock
	git status

generate:
  poetry run python scripts/parse.py
  black stacklet
