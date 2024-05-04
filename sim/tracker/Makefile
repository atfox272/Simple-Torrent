.PHONY: run clean

# Define the Python interpreter to use
PYTHON := python3

# Define the name of your main Python file
MAIN_FILE := tracker_server.py

# Define any dependencies (e.g., requirements.txt for pip)
REQUIREMENTS := requirements.txt

# Define the name of your virtual environment
VENV := .venv

# Target to install dependencies
install: $(REQUIREMENTS)
	cp ../../tracker/tracker_server.py ./
	$(PYTHON) -m pip install -r $(REQUIREMENTS)

# Target to run the main Python script
run: $(MAIN_FILE)
	$(PYTHON) $(MAIN_FILE)

# Target to create a virtual environment
venv:
	$(PYTHON) -m venv $(VENV)

# Target to clean up generated files and folders
clean:
	rm *.py
	rm -rf $(VENV) __pycache__

rerun:
	make clean
	make install
	make run

# Default target
.DEFAULT_GOAL := run
