lint:
	uv run ruff check --fix && uv run ruff format

test:
	uv run pytest

udoc:
	uv run python scripts/update_provider_catalog.py
