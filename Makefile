FLAKE_IGNORES := W503,E203
FLAKE_EXCLUSIONS := .git,venv,.vscode,.pytest_cache,ideas.py
FLAKE_EXTRAS := --jobs 1 --max-line-length 120

.PHONY: black isort flake reformat

## Applies black formatter.
black:
	black --line-length 120 --verbose --experimental-string-processing .
	@echo "black finished successfully"

## Applies isort formatter in import statements.
isort:
	isort --verbose .
	@echo "isort finished successfully"

## Python linting quality control.
flake:
	flake8 . $(FLAKE_EXTRAS) --ignore $(FLAKE_IGNORES) --exclude $(FLAKE_EXCLUSIONS)
	@echo "flake finished successfully"

reformat: isort black flake
	@echo "Reformatting finished successfully"