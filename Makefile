.PHONY: install test lint format type-check run docker-build docker-up clean coverage

install:
	pip install -r requirements.txt

test:
	pytest tests/ -v --tb=short

coverage:
	pytest tests/ -v --tb=short --cov=analysis --cov=api --cov=database --cov=scraper \
		--cov-report=term-missing --cov-report=html
	@echo "Coverage report in htmlcov/index.html"

lint:
	ruff check . --select E,F,W,I --ignore E501

format:
	ruff format .

lint-fix:
	ruff check . --select E,F,W,I --ignore E501 --fix

type-check:
	mypy analysis/ api/ database/ --ignore-missing-imports --no-error-summary

run:
	uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload

docker-build:
	docker build -t stock-market-intelligence .

docker-up:
	docker-compose up -d

docker-down:
	docker-compose down

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	rm -rf .coverage coverage.xml htmlcov/ .pytest_cache/ .mypy_cache/

help:
	@echo "Available targets:"
	@echo "  install      Install dependencies"
	@echo "  test         Run test suite"
	@echo "  coverage     Run tests with coverage report"
	@echo "  lint         Run ruff linter"
	@echo "  format       Run ruff formatter"
	@echo "  lint-fix     Run ruff with auto-fix"
	@echo "  type-check   Run mypy type checking"
	@echo "  run          Start API server"
	@echo "  docker-build Build Docker image"
	@echo "  docker-up    Start with Docker Compose"
	@echo "  docker-down  Stop Docker Compose"
	@echo "  clean        Remove cache files"
