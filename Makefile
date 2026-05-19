NAME = a_maze_ing
PIP := ./venv/bin/pip
PYTHON := ./venv/bin/python3

REQS = requirements.txt
SRC = a_maze_ing.py mazegen/maze_generator.py representation.py

.PHONY: all install build run debug clean lint

all: install run

install:
	python3 -m venv venv
	$(PIP) install --upgrade pip	
	@echo "Installing dependencies..."
	@if [ -f $(REQS) ]; then $(PIP) install -r $(REQS); else echo "No requirements.txt found, skipping."; fi

build:
	$(PYTHON) -m build


run:
	@echo "Running the project..."
	$(PYTHON) a_maze_ing.py config.txt

debug:
	@echo "Running in debug mode..."
	$(PYTHON) -m pdb a_maze_ing.py config.txt
	
clean:
	@echo "Cleaning temporary files..."
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .mypy_cache -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .pytest_cache -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	rm -rf build/ dist/ 2>/dev/null || true


lint:
	$(PYTHON) -m flake8 $(SRC)
	$(PYTHON) -m mypy $(SRC) \
	--warn-return-any \
	--warn-unused-ignores \
	--ignore-missing-imports \
	--disallow-untyped-defs \
	--check-untyped-defs



