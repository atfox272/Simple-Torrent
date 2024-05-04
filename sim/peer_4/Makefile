.PHONY: run clean

# Define the Python interpreter to use
PYTHON := python3

# Define the name of your main Python file
MAIN_FILE := peer_proc.py

# Define any dependencies (e.g., requirements.txt for pip)
REQUIREMENTS := requirements.txt

# Define the name of your virtual environment
VENV := .venv

# Target to install dependencies
install: $(REQUIREMENTS)
	cp ../../peer/*.py ./
	cp ../../peer/sim_data_folder/for_peer_4/* ./
	cp -r ../../peer/pieces_folder ./
	cp -r ../../peer/metainfo_folder ./
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
	rm hehe.txt
	rm *.json
	rm -r */

rerun:
	make clean
	make install
	make run

# Default target
.DEFAULT_GOAL := run
