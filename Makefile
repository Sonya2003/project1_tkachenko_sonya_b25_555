install:
	poetry install
project:
	poetry run python3 ./labyrinth_game/main.py
build:
	poetry build
publish:
	poetry publish --dry-run 
package-install:
	python3 -m pip install dist/*.whl
lint:
	poetry run ruff check .
format:
	poetry run ruff format .
clean:
	rm -rf __pycache__ .pytest_cache *.egg-info
