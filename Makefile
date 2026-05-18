# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Makefile                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: romarti2 <romarti2@student.42madrid.com    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2026/03/02 17:55:29 by romarti2          #+#    #+#              #
#    Updated: 2026/05/18 18:38:25 by romarti2         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

NAME = a_maze_ing
PIP := ./venv/bin/pip
PYTHON := ./venv/bin/python3

REQS = requirements.txt # Mirar esto, poner liberias si usamos

SRC = a_maze_ing.py maze_generator.py representation.py

all: install build run

install:
	python3 -m venv venv
	$(PIP) install --upgrade pip	
	@echo "Installing dependencies..."
	@if [ -f $(REQS) ]; then $(PIP) install -r $(REQS); else echo "No requirements.txt found, skipping."; fi

build:
	. ./venv/bin/activate && $(PYTHON) -m build


run:
	@echo "Running the project..."
	. ./venv/bin/activate && $(PYTHON) a_maze_ing.py config.txt

debug:
	@echo "Running in debug mode..."
	. ./venv/bin/activate && $(PYTHON) -m pytest -v
	
clean:
	@echo "Cleaning temporary files..."
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .mypy_cache -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .pytest_cache -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	rm -rf build/ dist/ 2>/dev/null || true


lint:
	@echo "Running lint checks..."
	-flake8 *.py */*.py 
	mypy *.py */*.py \
	--warn-return-any \
	--warn-unused-ignores \
	--ignore-missing-imports \
	--disallow-untyped-defs \
	--check-untyped-defs \


.PHONY: all install build run debug clean lint build