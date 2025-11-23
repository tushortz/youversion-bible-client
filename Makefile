.PHONY: help install install-dev test test-cov test-verbose test-fast test-unit test-integration lint lint-fix format format-check check fix clean build docs docs-clean docs-serve cli-help cli-votd cli-moments cli-highlights cli-notes cli-bookmarks cli-images cli-plan-progress cli-plan-subscriptions dev-setup pre-commit ci-test ci-lint clean-all

# Default target
help:
	@echo "YouVersion Bible Client - Makefile Commands"
	@echo "============================================"
	@echo ""
	@echo "Installation:"
	@echo "  make install          Install production dependencies"
	@echo "  make install-dev      Install development dependencies"
	@echo ""
	@echo "Testing:"
	@echo "  make test             Run tests"
	@echo "  make test-cov         Run tests with coverage"
	@echo "  make test-verbose     Run tests with verbose output"
	@echo "  make test-fast        Run fast tests (skip slow)"
	@echo "  make test-unit        Run unit tests only"
	@echo "  make test-integration Run integration tests only"
	@echo ""
	@echo "Code Quality:"
	@echo "  make lint             Run linter (ruff)"
	@echo "  make lint-fix         Auto-fix linting issues"
	@echo "  make format           Format code (black)"
	@echo "  make format-check     Check code formatting"
	@echo "  make check            Run lint and format check"
	@echo "  make fix              Format and fix lint issues"
	@echo ""
	@echo "Documentation:"
	@echo "  make docs             Build documentation"
	@echo "  make docs-clean       Clean documentation build"
	@echo "  make docs-serve       Serve documentation locally"
	@echo ""
	@echo "Build & Clean:"
	@echo "  make build            Build package"
	@echo "  make clean            Clean build artifacts"
	@echo "  make clean-all        Clean all generated files"
	@echo ""
	@echo "CLI Commands:"
	@echo "  make cli-help         Show CLI help"
	@echo "  make cli-votd         Get verse of the day"
	@echo "  make cli-moments      Get moments"
	@echo "  make cli-highlights   Get highlights"
	@echo "  make cli-notes        Get notes"
	@echo "  make cli-bookmarks    Get bookmarks"
	@echo "  make cli-images       Get images"
	@echo "  make cli-plan-progress Get plan progress"
	@echo ""
	@echo "Development:"
	@echo "  make dev-setup        Setup development environment"
	@echo "  make pre-commit       Run pre-commit checks"
	@echo "  make ci-test          Run CI test suite"
	@echo "  make ci-lint          Run CI linting"
	@echo ""

# Installation
install:
	poetry install --no-dev

install-dev:
	poetry install

# Testing
test:
	poetry run pytest

test-cov:
	poetry run pytest --cov=youversion --cov-report=html --cov-report=term

test-verbose:
	poetry run pytest -v

test-fast:
	poetry run pytest -m "not slow"

test-unit:
	poetry run pytest -m unit

test-integration:
	poetry run pytest -m integration

# Code Quality
lint:
	poetry run ruff check youversion tests

lint-fix:
	poetry run ruff check --fix youversion tests

format:
	poetry run black youversion tests

format-check:
	poetry run black --check youversion tests

check: lint format-check
	@echo "✓ All checks passed"

fix: format lint-fix
	@echo "✓ Code formatted and lint issues fixed"

# Documentation
docs:
	cd documentation && poetry run make html

docs-clean:
	cd documentation && poetry run make clean

docs-serve:
	cd documentation && poetry run make html && open build/html/index.html

# Build & Clean
build:
	poetry build

clean:
	rm -rf build dist *.egg-info .pytest_cache .coverage htmlcov
	find . -type d -name __pycache__ -exec rm -r {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete

clean-all: clean docs-clean
	rm -rf .ruff_cache .mypy_cache

# CLI Commands (examples - modify as needed)
cli-help:
	poetry run youversion --help

cli-votd:
	poetry run youversion votd

cli-moments:
	poetry run youversion moments

cli-highlights:
	poetry run youversion highlights

cli-notes:
	poetry run youversion notes

cli-bookmarks:
	poetry run youversion bookmarks

cli-images:
	poetry run youversion images

cli-plan-progress:
	poetry run youversion plan-progress

cli-plan-subscriptions:
	poetry run youversion plan-subscriptions

# Development workflow
dev-setup: install-dev
	@echo "✓ Development environment setup complete"

pre-commit: format lint test
	@echo "✓ Pre-commit checks passed"

# CI/CD helpers
ci-test: test-cov
	@echo "✓ CI tests completed"

ci-lint: lint format-check
	@echo "✓ CI linting completed"

