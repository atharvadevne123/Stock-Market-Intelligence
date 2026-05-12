.PHONY: install test lint format type-check run docker-build docker-up clean coverage audit

install:
	pip install -r requirements.txt

install-dev:
	pip install -r requirements.txt
	pip install pre-commit
	pre-commit install

test:
	pytest tests/ -v --tb=short -p no:warnings

coverage:
	pytest tests/ -v --tb=short -p no:warnings \
		--cov=analysis --cov=api --cov=database --cov=scraper \
		--cov-report=term-missing --cov-report=html
	@echo "Coverage report: htmlcov/index.html"

lint:
	ruff check . --select E,F,W,I --ignore E501

format:
	ruff format .

lint-fix:
	ruff check . --select E,F,W,I --ignore E501 --fix

type-check:
	mypy analysis/ api/ database/ --ignore-missing-imports --no-error-summary

audit:
	pip install pip-audit -q
	pip-audit -r requirements.txt

run:
	uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload

run-prod:
	uvicorn api.main:app --host 0.0.0.0 --port 8000 --workers 4

docker-build:
	docker build -t stock-market-intelligence .

docker-up:
	docker-compose up -d

docker-down:
	docker-compose down

docker-logs:
	docker-compose logs -f api

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	rm -rf .coverage coverage.xml htmlcov/ .pytest_cache/ .mypy_cache/

help:
	@echo "Available targets:"
	@echo "  install      Install all dependencies"
	@echo "  install-dev  Install deps + pre-commit hooks"
	@echo "  test         Run test suite"
	@echo "  coverage     Run tests with HTML coverage report"
	@echo "  lint         Lint with ruff"
	@echo "  format       Format with ruff"
	@echo "  lint-fix     Auto-fix lint errors"
	@echo "  type-check   Run mypy"
	@echo "  audit        Security audit of dependencies"
	@echo "  run          Start API server (dev)"
	@echo "  run-prod     Start API server (production, 4 workers)"
	@echo "  docker-build Build Docker image"
	@echo "  docker-up    Start with Docker Compose"
	@echo "  docker-down  Stop Docker Compose"
	@echo "  clean        Remove build and cache files"
