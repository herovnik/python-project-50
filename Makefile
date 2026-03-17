gendiff:
	uv run gendiff

build:
	uv build

package-install:
	uv tool install dist/*.whl

good:
	uv build
	uv tool install dist/*.whl
	uv run ruff check
	uv run pytest

send:
	git add .
	git commit -m "add some features"
	git push -u origin main

lint:
	uv run ruff check

test:
	uv run pytest
