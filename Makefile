PYTHON = python3

install:
	pip install pygame

run :
	$(PYTHON) main.py

clean :
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true

re : clean run

.PHONY : run clean