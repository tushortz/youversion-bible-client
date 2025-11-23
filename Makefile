.PHONY: help install install-dev test test-cov test-verbose test-fast test-unit test-integration lint lint-fix format format-check check fix clean build docs docs-clean docs-serve cli-help cli-votd cli-moments cli-highlights cli-notes cli-bookmarks cli-images cli-plan-progress cli-plan-subscriptions dev-setup pre-commit ci-test ci-lint clean-all update lock shell type-check security-check run-example run-examples deps deps-update deps-outdated deps-tree version bump-version bump-patch bump-minor bump-major release release-check publish publish-test publish-prod env env-info env-remove coverage coverage-html coverage-report coverage-open watch-test watch-lint watch-format validate validate-all

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
	@echo "  make cli-help              Show CLI help"
	@echo "  make cli-votd              Get verse of the day"
	@echo "  make cli-moments           Get moments"
	@echo "  make cli-highlights        Get highlights"
	@echo "  make cli-notes             Get notes"
	@echo "  make cli-bookmarks         Get bookmarks"
	@echo "  make cli-images            Get images"
	@echo "  make cli-plan-progress     Get plan progress"
	@echo "  make cli-plan-subscriptions Get plan subscriptions"
	@echo "  make cli-plan-completions  Get plan completions"
	@echo "  make cli-create-moment     Create a moment"
	@echo ""
	@echo "Dependencies:"
	@echo "  make deps                  Show dependency tree"
	@echo "  make deps-update           Update dependencies"
	@echo "  make deps-outdated         Show outdated dependencies"
	@echo "  make deps-tree             Show dependency tree"
	@echo "  make update                Update lock file"
	@echo "  make lock                  Lock dependencies"
	@echo ""
	@echo "Environment:"
	@echo "  make shell                 Start Poetry shell"
	@echo "  make env                   Show environment info"
	@echo "  make env-info              Show Poetry environment info"
	@echo "  make env-remove            Remove Poetry environment"
	@echo ""
	@echo "Code Quality (Extended):"
	@echo "  make type-check            Run type checking (mypy)"
	@echo "  make security-check        Run security checks"
	@echo "  make validate              Run all validation checks"
	@echo "  make validate-all          Run full validation suite"
	@echo ""
	@echo "Testing (Extended):"
	@echo "  make coverage              Run tests with coverage"
	@echo "  make coverage-html         Generate HTML coverage report"
	@echo "  make coverage-report       Show coverage report"
	@echo "  make coverage-open         Open coverage report in browser"
	@echo "  make watch-test            Watch for changes and run tests"
	@echo "  make watch-lint            Watch for changes and run linter"
	@echo "  make watch-format          Watch for changes and format"
	@echo ""
	@echo "Examples:"
	@echo "  make run-example            Run basic usage example"
	@echo "  make run-examples           Run all examples"
	@echo ""
	@echo "Version & Release:"
	@echo "  make version               Show current version"
	@echo "  make bump-version          Bump version (interactive)"
	@echo "  make bump-patch            Bump patch version (0.1.0 -> 0.1.1)"
	@echo "  make bump-minor            Bump minor version (0.1.0 -> 0.2.0)"
	@echo "  make bump-major            Bump major version (0.1.0 -> 1.0.0)"
	@echo "  make release               Prepare release"
	@echo "  make release-check         Check release readiness"
	@echo "  make publish               Publish to PyPI (test)"
	@echo "  make publish-test          Publish to TestPyPI"
	@echo "  make publish-prod          Publish to PyPI (production)"
	@echo ""
	@echo "Development:"
	@echo "  make dev-setup              Setup development environment"
	@echo "  make pre-commit             Run pre-commit checks"
	@echo "  make ci-test                Run CI test suite"
	@echo "  make ci-lint                Run CI linting"
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

cli-plan-completions:
	poetry run youversion plan-completions

cli-create-moment:
	@echo "Usage: make cli-create-moment KIND='note' CONTENT='...' TITLE='...'"
	@echo "Example: make cli-create-moment KIND='note' CONTENT='Test' TITLE='My Note'"
	@if [ -z "$(KIND)" ] || [ -z "$(CONTENT)" ] || [ -z "$(TITLE)" ]; then \
		echo "Error: KIND, CONTENT, and TITLE are required"; \
		exit 1; \
	fi
	poetry run youversion create-moment --kind $(KIND) --content "$(CONTENT)" --title "$(TITLE)"


# Dependencies
deps:
	poetry show

deps-update:
	poetry update

deps-outdated:
	poetry show --outdated

deps-tree:
	poetry show --tree

update:
	poetry lock

lock:
	poetry lock

# Environment
shell:
	poetry shell

env:
	@echo "Python version:"
	@poetry run python --version
	@echo "\nPoetry environment:"
	@poetry env info

env-info:
	poetry env info

env-remove:
	poetry env remove --all

# Code Quality (Extended)
type-check:
	@if command -v mypy >/dev/null 2>&1; then \
		poetry run mypy youversion --ignore-missing-imports; \
	else \
		echo "⚠️  mypy not installed. Install with: poetry add --group dev mypy"; \
	fi

security-check:
	@if command -v bandit >/dev/null 2>&1; then \
		poetry run bandit -r youversion -f json -o bandit-report.json || true; \
		poetry run bandit -r youversion; \
	else \
		echo "⚠️  bandit not installed. Install with: poetry add --group dev bandit[toml]"; \
	fi

validate: lint format-check
	@echo "✓ Validation checks passed"

validate-all: lint format-check type-check test
	@echo "✓ All validation checks passed"

# Testing (Extended)
coverage: test-cov

coverage-html:
	poetry run pytest --cov=youversion --cov-report=html
	@echo "✓ Coverage report generated in htmlcov/index.html"

coverage-report:
	poetry run pytest --cov=youversion --cov-report=term-missing

coverage-open: coverage-html
	@if command -v open >/dev/null 2>&1; then \
		open htmlcov/index.html; \
	elif command -v xdg-open >/dev/null 2>&1; then \
		xdg-open htmlcov/index.html; \
	else \
		echo "Please open htmlcov/index.html in your browser"; \
	fi

watch-test:
	@if command -v entr >/dev/null 2>&1; then \
		find youversion tests -name "*.py" | entr -c poetry run pytest; \
	else \
		echo "⚠️  entr not installed. Install with: brew install entr (macOS) or apt-get install entr (Linux)"; \
	fi

watch-lint:
	@if command -v entr >/dev/null 2>&1; then \
		find youversion tests -name "*.py" | entr -c poetry run ruff check youversion tests; \
	else \
		echo "⚠️  entr not installed. Install with: brew install entr (macOS) or apt-get install entr (Linux)"; \
	fi

watch-format:
	@if command -v entr >/dev/null 2>&1; then \
		find youversion tests -name "*.py" | entr -c poetry run black youversion tests; \
	else \
		echo "⚠️  entr not installed. Install with: brew install entr (macOS) or apt-get install entr (Linux)"; \
	fi

# Examples
run-example:
	poetry run python examples/basic_usage.py

run-examples:
	@echo "Running all examples..."
	@for example in examples/*.py; do \
		if [ -f "$$example" ] && [ "$$example" != "examples/README.md" ]; then \
			echo "\n=== Running $$example ==="; \
			poetry run python "$$example" || true; \
		fi \
	done

# Version & Release
version:
	@poetry version

bump-version:
	@read -p "Enter new version (e.g., 0.2.0): " version; \
	poetry version $$version

bump-patch:
	poetry version patch
	@echo "✓ Version bumped to $(shell poetry version -s)"

bump-minor:
	poetry version minor
	@echo "✓ Version bumped to $(shell poetry version -s)"

bump-major:
	poetry version major
	@echo "✓ Version bumped to $(shell poetry version -s)"

release:
	@echo "Preparing release..."
	@echo "Current version: $(shell poetry version -s)"
	@echo "Running validation checks..."
	@make validate-all
	@echo "Building package..."
	@make build
	@echo "✓ Release prepared. Version: $(shell poetry version -s)"

release-check:
	@echo "Checking release readiness..."
	@echo "Version: $(shell poetry version -s)"
	@make validate-all
	@echo "✓ Release checks passed"

publish:
	@echo "⚠️  This will publish to TestPyPI. Use 'make publish-prod' for production."
	@make publish-test

publish-test:
	@echo "Publishing to TestPyPI..."
	poetry publish --repository testpypi

publish-prod:
	@echo "⚠️  Publishing to PyPI (production)..."
	@read -p "Are you sure? [y/N] " -n 1 -r; \
	echo; \
	if [[ $$REPLY =~ ^[Yy]$$ ]]; then \
		poetry publish; \
	else \
		echo "Publishing cancelled."; \
	fi

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

