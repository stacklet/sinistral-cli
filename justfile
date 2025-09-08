default:
	@just --list

install:
	uv sync
	uv run pre-commit install

test *flags:
	uv run pytest --cov=stacklet {{ flags }}

pkg-prep bump="--bump-patch":
	uv run python scripts/upgrade.py upgrade {{bump}}
	uv lock --upgrade
	git add justfile pyproject.toml uv.lock
	git status

generate:
  uv run python scripts/parse.py
  black stacklet
