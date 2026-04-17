PYTHON := python3
VENV := .venv
PIP := $(VENV)/bin/pip
PY := $(VENV)/bin/python
PLAYWRIGHT := $(VENV)/bin/playwright

.PHONY: help venv install browser setup freeze clean

help:
	@echo "Available targets:"
	@echo "  make venv      - create virtual environment"
	@echo "  make install   - install Python dependencies"
	@echo "  make browser   - install Playwright browsers"
	@echo "  make setup     - full setup (venv + deps + browsers)"
	@echo "  make freeze    - write current deps to requirements.txt"
	@echo "  make clean     - remove virtual environment"

venv:
	$(PYTHON) -m venv $(VENV)

install: venv
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

browser: install
	$(PLAYWRIGHT) install

setup: browser

freeze: venv
	$(PIP) freeze > requirements.txt

clean:
	rm -rf $(VENV)