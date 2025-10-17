lint:
	uv run ruff check --fix && uv run ruff format

test:
	uv run pytest

udoc:
	uv run python scripts/update_provider_catalog.py

ui:
	uv run uvicorn examples.ui.app:app --reload --port 5004

docs:
	uv run mkdocs serve --config-file mkdocs/mkdocs.yml

docsb:
	uv run mkdocs build --config-file mkdocs/mkdocs.yml