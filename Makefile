# Makefile for hello-python project

.PHONY: help install test lint format clean

help:
	@echo "可用命令:"
	@echo "  make install    安装依赖"
	@echo "  make test       运行测试"
	@echo "  make lint       代码检查"
	@echo "  make format     代码格式化"
	@echo "  make clean      清理临时文件"

install:
	pip install -e .
	pip install -r requirements.txt

test:
	pytest tests/ -v --cov=src --cov-report=html

lint:
	flake8 src/ tests/
	mypy src/

format:
	black src/ tests/
	isort src/ tests/

clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".coverage" -exec rm -rf {} +
	find . -type d -name "htmlcov" -exec rm -rf {} +
