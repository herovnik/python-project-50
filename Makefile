gendiff:
	uv run gendiff

build:
	uv build

package-install:
	uv tool install dist/*.whl
