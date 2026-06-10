# Makefile for hello-python project

.PHONY: help install test lint format clean

help:
	@echo "Available commands:"
	@echo "  make install    Install dependencies"
	@echo "  make test       Run tests"
	@echo "  make lint       Lint code"
	@echo "  make format     Format code"
	@echo "  make clean      Clean temp files"

install:
	pip install -e .
	pip install -r requirements.txt

test:
	pytest tests/ -v --cov=src --cov-report=html

lint:
	flake8 src/ tests/ --max-line-length=88 --exclude=codes/,doc/,docs/,examples/,scripts/
	mypy src/

format:
	black src/ tests/
	isort src/ tests/

clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	rm -rf .coverage htmlcov
