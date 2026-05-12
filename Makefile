# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Makefile                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: romarti2 <romarti2@student.42madrid.com    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2026/03/02 17:55:29 by romarti2          #+#    #+#              #
#    Updated: 2026/05/12 13:38:54 by romarti2         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

NAME = a_maze_ing
PYTHON = python3
PIP = pip3
PIPX = pipx

REQS = requirements.txt # Mirar esto, poner liberias si usamos

SRC = a_maze_ing.py maze_generator.py output_validator.py representation.py

CLEAN_DIRS = .mypy_cache

all: install run

install:
	@echo "Installing dependencies..."
	@if [ -f $(REQS) ]; then $(PIP) install -r $(REQS); else echo "No requirements.txt found, skipping."; fi

run:
	@echo "Running the project..."
	$(PYTHON) a_maze_ing.py config.txt

debug:
	@echo "Running in debug mode..."
	$(PYTHON) -m pdb a_maze_ing.py config.txt
	
clean:
	@echo "Cleaning temporary files..."
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -rf $(CLEAN_DIRS)

fclean: clean
	@echo "Full clean done."

re: fclean all

lint:
	@echo "Running lint checks..."
	-$(PYTHON) -m flake8 .
	$(PYTHON) -m mypy \
	--warn-return-any \
	--warn-unused-ignores \
	--ignore-missing-imports \
	--disallow-untyped-defs \
	--check-untyped-defs \
	.

lint-strict:
	@echo "Running strict lint checks..."
	-$(PYTHON) -m flake8 .
	$(PYTHON) -m mypy . --strict

.PHONY: all install run debug clean fclean re lint lint-strict
