*This project has been created as part of the 42 curriculum by romarti2, dtaylor-.*

# Amazing

## Description

Amazing is a maze generation and exploration project developed as part of the 42 curriculum.  
The goal of the project is to generate valid mazes using a deterministic algorithm, represent them through a configurable format, and provide tools to visualize and test the generated structures.

The project focuses on:
- Procedural maze generation
- File parsing and configuration handling
- Graph traversal and path validation
- Modular and reusable architecture
- Team collaboration and project organization

The generated mazes guarantee connectivity between the start and the exit while respecting the project constraints and map format.

---

# Features

- Random maze generation
- Configurable maze dimensions
- Valid path generation
- Wall and corridor representation
- Config file parsing
- Error handling for invalid maps/configurations
- Reusable utility modules
- Clean modular architecture

---

# Instructions

## Compilation

Compile the project using: make

Install dependencies: make install

Debug the project: make debug

Clean object files: make clean

Check for flake8 and mypy errors: make lint

Check for flake8 and mypy --strict: make lint-strict

# Configuration File Structure

The configuration file defines the maze parameters and generation settings.

Example:

| Parameter | Description |
|------------|-------------|
| WIDTH | Maze width |
| HEIGHT | Maze height |
| START_X | Starting X coordinate |
| START_Y | Starting Y coordinate |
| END_X | Exit X coordinate |
| END_Y | Exit Y coordinate |

# Maze Generation Algorithm
## Chosen Algorithm

This project uses the Recursive Backtracking Algorithm for maze generation, called Depth First Search (DFS).

## How it works
1. Start from an initial cell.
2. Randomly select an unvisited neighboring cell.
3. Remove the wall between both cells.
4. Continue recursively from the new cell.
5. Backtrack when no unvisited neighbors remain.


## Why We Chose This Algorithm

We selected recursive backtracking because:

- It is simple to implement and debug.
- It generates perfect mazes (without isolated sections).
- It guarantees full connectivity.
- It produces visually interesting maze patterns.
- It fits well with recursive and graph-based programming concepts taught at 42.

Additionally, it offers good performance for medium-sized mazes while remaining easy to maintain and extend.

# Reusable Module: mazegen

## How to Rebuild the Package From Source

To verify the build process in a clean environment (virtualenv or venv), run the following commands from the root of the repository:

1. python3 -m venv venv
2. source venv/bin/activate
3. pip install --upgrade pip build
4. python3 -m build


*The mazegen package exposes the MazeGenerator class, allowing you to customize, generate, and extract maze structures along with their solutions.*


## Basic Usage & Instantiation

Install locally the Package:

pip install dist/mazegen_romarti2dtaylor--1.0.0-py3-none-any.whl

# Team & Project Management
## Team Roles
*romarti2 and dtaylor-*
- Project architecture
- Core logic implementation
- Testing and validation
- Documentation
- Integration

*dtaylor-*
- Maze generation algorithm
- Parsing system
- Error handling

*romarti2*
- Visualization
- Code review


## The team used:

- Git branches for feature development
- Pull requests and code reviews
- Shared coding conventions
- Task division by modules
- Regular synchronization meetings

## Project Planning

### Initial Planning

At the beginning of the project, the team divided the work into several stages:

1. Research maze generation algorithms
2. Define the project architecture
3. Implement the parser and configuration system
4. Develop the maze generation logic
5. Add validation and error handling
6. Perform testing and optimization
7. Write documentation and finalize the project

The original objective was to first create a minimal working maze generator and progressively improve modularity and additional features.

---

### Evolution During Development

As development progressed, the planning evolved in several ways:

- More time than expected was spent debugging edge cases related to maze boundaries and invalid configurations.
- Additional helper utilities were added to simplify testing and debugging.
- Team coordination improved after introducing stricter branch management and code reviews.

The project structure became cleaner over time as modules were progressively separated by responsibility.

---

## What Worked Well

- Clear task distribution between team members
- Modular architecture
- Early testing of core features
- Frequent Git commits and branch separation
- Reusable utility functions
- Consistent coding style across modules

---

## What Could Be Improved

- Earlier integration testing between modules
- More automated tests
- Improved documentation during development instead of only at the end
- Better anticipation of merge conflicts in collaborative work

## Resources
### Documentation & References

- GeeksforGeeks maze generation articles
- Wikipedia — Maze generation algorithms
- Stack Overflow discussions related to recursion and graph traversal
 ### AI Usage

AI tools were used as assistance during the project for:

- README structure and documentation drafting
- Clarification of maze generation concepts
- Suggestions for code organization
- Documentation wording
