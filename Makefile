# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Makefile                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: romarti2 <romarti2@student.42madrid.com    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2026/03/02 17:55:29 by romarti2          #+#    #+#              #
#    Updated: 2026/05/11 16:27:15 by romarti2         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

NAME = a_maze_ing
PYTHON = python3
PIP = pip
PIPX = pipx

REQS = requirements.txt # Mirar esto, poner liberias si usamos

SRC = a_maze_ing.py maze_generator.py output_validator.py representation.py

CLEAN_DIRS = __pycache__ .mypy_cache

all: install run

install:
	@echo "Installing dependencies..."
	@if [ -f $(REQS) ]; then $(PIP) install -r $(REQS); else echo "No requirements.txt found, skipping."; fi

run:
	@echo "Running the project..."
	$(PYTHON) a_maze_ing.py config.txt

clean:
	@echo "Cleaning temporary files..."
	rm -rf $(CLEAN_DIRS)

fclean: clean
	@echo "Full clean done."

re: fclean all

lint:
	@echo "Running lint checks..."
	flake8 .
	mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports \
	--disallow-untyped-defs --check-untyped-defs

lint-strict:
	@echo "Running strict lint checks..."
	flake8 .
	mypy . --strict

.PHONY: all install run debug clean lint lint-strict
