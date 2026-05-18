PYTHON = python3
FILE ?=

install:
	pip install pygame
	pip install mypy flake8

run :
	$(PYTHON) main.py $(FILE)

clean :
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true

re : clean run

lint:
	flake8 .
	mypy . --warn-return-any \
	--warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs \
	--check-untyped-defs

.PHONY: install run clean re lint