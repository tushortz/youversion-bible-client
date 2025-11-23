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
	@echo "  Moments & Content:"
	@echo "    make cli-votd              Get verse of the day"
	@echo "    make cli-moments           Get moments"
	@echo "    make cli-highlights        Get highlights"
	@echo "    make cli-notes             Get notes"
	@echo "    make cli-bookmarks         Get bookmarks"
	@echo "    make cli-images            Get images"
	@echo "    make cli-badges            Get badges"
	@echo "    make cli-create-moment     Create a moment"
	@echo "    make cli-convert-notes     Convert notes to markdown"
	@echo "  Plans:"
	@echo "    make cli-plan-progress     Get plan progress"
	@echo "    make cli-plan-subscriptions Get plan subscriptions"
	@echo "    make cli-plan-completions  Get plan completions"
	@echo "  Bible & Audio:"
	@echo "    make cli-get-bible-configuration Get Bible configuration"
	@echo "    make cli-get-bible-versions Get Bible versions"
	@echo "    make cli-get-bible-version Get Bible version by ID"
	@echo "    make cli-get-bible-chapter Get Bible chapter"
	@echo "    make cli-get-recommended-languages Get recommended languages"
	@echo "    make cli-get-audio-chapter Get audio chapter"
	@echo "    make cli-get-audio-version Get audio version"
	@echo "  Search:"
	@echo "    make cli-search-bible      Search Bible"
	@echo "    make cli-search-plans      Search plans"
	@echo "    make cli-search-users      Search users"
	@echo "  Videos & Images:"
	@echo "    make cli-get-videos        Get videos"
	@echo "    make cli-get-video-details Get video details"
	@echo "    make cli-get-images        Get images"
	@echo "    make cli-get-image-upload-url Get image upload URL"
	@echo "  Events:"
	@echo "    make cli-search-events     Search events"
	@echo "    make cli-get-event-details Get event details"
	@echo "    make cli-get-saved-events  Get saved events"
	@echo "    make cli-save-event       Save event"
	@echo "    make cli-delete-saved-event Delete saved event"
	@echo "    make cli-get-all-saved-event-ids Get all saved event IDs"
	@echo "    make cli-get-event-configuration Get event configuration"
	@echo "  Moments Management:"
	@echo "    make cli-get-moments       Get moments"
	@echo "    make cli-get-moment-details Get moment details"
	@echo "    make cli-update-moment     Update moment"
	@echo "    make cli-delete-moment     Delete moment"
	@echo "    make cli-get-moment-colors Get moment colors"
	@echo "    make cli-get-moment-labels Get moment labels"
	@echo "    make cli-get-verse-colors  Get verse colors"
	@echo "    make cli-hide-verse-colors Hide verse colors"
	@echo "    make cli-get-moments-configuration Get moments configuration"
	@echo "  Comments & Likes:"
	@echo "    make cli-create-comment    Create comment"
	@echo "    make cli-delete-comment    Delete comment"
	@echo "    make cli-like-moment       Like moment"
	@echo "    make cli-unlike-moment     Unlike moment"
	@echo "  Devices:"
	@echo "    make cli-register-device   Register device"
	@echo "    make cli-unregister-device Unregister device"
	@echo "  Themes:"
	@echo "    make cli-get-themes        Get themes"
	@echo "    make cli-add-theme         Add theme"
	@echo "    make cli-remove-theme      Remove theme"
	@echo "    make cli-set-theme         Set theme"
	@echo "    make cli-get-theme-description Get theme description"
	@echo "  Social:"
	@echo "    make cli-send-friend-request Send friend request"
	@echo "  Localization:"
	@echo "    make cli-get-localization-items Get localization items"
	@echo "  Help:"
	@echo "    make cli-help              Show CLI help"
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
	cd docs && poetry run make html

docs-clean:
	cd docs && poetry run make clean

docs-serve:
	cd docs && poetry run make html && open build/html/index.html

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

cli-badges:
	poetry run youversion badges

cli-convert-notes:
	poetry run youversion convert-notes

cli-get-bible-configuration:
	poetry run youversion get-bible-configuration

cli-get-bible-versions:
	poetry run youversion get-bible-versions

cli-get-bible-version:
	@echo "Usage: make cli-get-bible-version ID=1"
	@if [ -z "$(ID)" ]; then \
		echo "Error: ID is required"; \
		exit 1; \
	fi
	poetry run youversion get-bible-version $(ID)

cli-get-bible-chapter:
	@echo "Usage: make cli-get-bible-chapter REFERENCE='GEN.1' VERSION_ID=1"
	@if [ -z "$(REFERENCE)" ] || [ -z "$(VERSION_ID)" ]; then \
		echo "Error: REFERENCE and VERSION_ID are required"; \
		exit 1; \
	fi
	poetry run youversion get-bible-chapter $(REFERENCE) --version-id $(VERSION_ID)

cli-get-recommended-languages:
	poetry run youversion get-recommended-languages

cli-get-audio-chapter:
	@echo "Usage: make cli-get-audio-chapter REFERENCE='GEN.1' VERSION_ID=1"
	@if [ -z "$(REFERENCE)" ] || [ -z "$(VERSION_ID)" ]; then \
		echo "Error: REFERENCE and VERSION_ID are required"; \
		exit 1; \
	fi
	poetry run youversion get-audio-chapter $(REFERENCE) --version-id $(VERSION_ID)

cli-get-audio-version:
	@echo "Usage: make cli-get-audio-version ID=1"
	@if [ -z "$(ID)" ]; then \
		echo "Error: ID is required"; \
		exit 1; \
	fi
	poetry run youversion get-audio-version $(ID)

cli-search-bible:
	@echo "Usage: make cli-search-bible QUERY='love' VERSION_ID=1"
	@if [ -z "$(QUERY)" ]; then \
		echo "Error: QUERY is required"; \
		exit 1; \
	fi
	poetry run youversion search-bible "$(QUERY)" --version-id $(VERSION_ID)

cli-search-plans:
	@echo "Usage: make cli-search-plans QUERY='daily' LANGUAGE_TAG='en'"
	@if [ -z "$(QUERY)" ]; then \
		echo "Error: QUERY is required"; \
		exit 1; \
	fi
	poetry run youversion search-plans "$(QUERY)" --language-tag $(LANGUAGE_TAG)

cli-search-users:
	@echo "Usage: make cli-search-users QUERY='john'"
	@if [ -z "$(QUERY)" ]; then \
		echo "Error: QUERY is required"; \
		exit 1; \
	fi
	poetry run youversion search-users "$(QUERY)"

cli-get-videos:
	poetry run youversion get-videos

cli-get-video-details:
	@echo "Usage: make cli-get-video-details ID=123"
	@if [ -z "$(ID)" ]; then \
		echo "Error: ID is required"; \
		exit 1; \
	fi
	poetry run youversion get-video-details $(ID)

cli-get-images:
	poetry run youversion get-images

cli-get-image-upload-url:
	poetry run youversion get-image-upload-url

cli-search-events:
	@echo "Usage: make cli-search-events QUERY='church' LATITUDE=40.7128 LONGITUDE=-74.0060"
	@if [ -z "$(QUERY)" ]; then \
		echo "Error: QUERY is required"; \
		exit 1; \
	fi
	poetry run youversion search-events "$(QUERY)" --latitude $(LATITUDE) --longitude $(LONGITUDE)

cli-get-event-details:
	@echo "Usage: make cli-get-event-details ID=123"
	@if [ -z "$(ID)" ]; then \
		echo "Error: ID is required"; \
		exit 1; \
	fi
	poetry run youversion get-event-details $(ID)

cli-get-saved-events:
	poetry run youversion get-saved-events

cli-save-event:
	@echo "Usage: make cli-save-event ID=123"
	@if [ -z "$(ID)" ]; then \
		echo "Error: ID is required"; \
		exit 1; \
	fi
	poetry run youversion save-event $(ID)

cli-delete-saved-event:
	@echo "Usage: make cli-delete-saved-event ID=123"
	@if [ -z "$(ID)" ]; then \
		echo "Error: ID is required"; \
		exit 1; \
	fi
	poetry run youversion delete-saved-event $(ID)

cli-get-all-saved-event-ids:
	poetry run youversion get-all-saved-event-ids

cli-get-event-configuration:
	poetry run youversion get-event-configuration

cli-get-moments:
	poetry run youversion get-moments

cli-get-moment-details:
	@echo "Usage: make cli-get-moment-details ID=123"
	@if [ -z "$(ID)" ]; then \
		echo "Error: ID is required"; \
		exit 1; \
	fi
	poetry run youversion get-moment-details $(ID)

cli-update-moment:
	@echo "Usage: make cli-update-moment ID=123 CONTENT='...'"
	@if [ -z "$(ID)" ] || [ -z "$(CONTENT)" ]; then \
		echo "Error: ID and CONTENT are required"; \
		exit 1; \
	fi
	poetry run youversion update-moment $(ID) --content "$(CONTENT)"

cli-delete-moment:
	@echo "Usage: make cli-delete-moment ID=123"
	@if [ -z "$(ID)" ]; then \
		echo "Error: ID is required"; \
		exit 1; \
	fi
	poetry run youversion delete-moment $(ID)

cli-get-moment-colors:
	poetry run youversion get-moment-colors

cli-get-moment-labels:
	poetry run youversion get-moment-labels

cli-get-verse-colors:
	poetry run youversion get-verse-colors

cli-hide-verse-colors:
	poetry run youversion hide-verse-colors

cli-get-moments-configuration:
	poetry run youversion get-moments-configuration

cli-create-comment:
	@echo "Usage: make cli-create-comment MOMENT_ID=123 BODY='...'"
	@if [ -z "$(MOMENT_ID)" ] || [ -z "$(BODY)" ]; then \
		echo "Error: MOMENT_ID and BODY are required"; \
		exit 1; \
	fi
	poetry run youversion create-comment $(MOMENT_ID) --body "$(BODY)"

cli-delete-comment:
	@echo "Usage: make cli-delete-comment MOMENT_ID=123 COMMENT_ID=456"
	@if [ -z "$(MOMENT_ID)" ] || [ -z "$(COMMENT_ID)" ]; then \
		echo "Error: MOMENT_ID and COMMENT_ID are required"; \
		exit 1; \
	fi
	poetry run youversion delete-comment $(MOMENT_ID) $(COMMENT_ID)

cli-like-moment:
	@echo "Usage: make cli-like-moment ID=123"
	@if [ -z "$(ID)" ]; then \
		echo "Error: ID is required"; \
		exit 1; \
	fi
	poetry run youversion like-moment $(ID)

cli-unlike-moment:
	@echo "Usage: make cli-unlike-moment ID=123"
	@if [ -z "$(ID)" ]; then \
		echo "Error: ID is required"; \
		exit 1; \
	fi
	poetry run youversion unlike-moment $(ID)

cli-register-device:
	@echo "Usage: make cli-register-device TOKEN='...' PLATFORM='android'"
	@if [ -z "$(TOKEN)" ] || [ -z "$(PLATFORM)" ]; then \
		echo "Error: TOKEN and PLATFORM are required"; \
		exit 1; \
	fi
	poetry run youversion register-device --token "$(TOKEN)" --platform $(PLATFORM)

cli-unregister-device:
	@echo "Usage: make cli-unregister-device TOKEN='...'"
	@if [ -z "$(TOKEN)" ]; then \
		echo "Error: TOKEN is required"; \
		exit 1; \
	fi
	poetry run youversion unregister-device --token "$(TOKEN)"

cli-get-themes:
	poetry run youversion get-themes

cli-add-theme:
	@echo "Usage: make cli-add-theme ID=1 LANGUAGE_TAG='eng'"
	@if [ -z "$(ID)" ] || [ -z "$(LANGUAGE_TAG)" ]; then \
		echo "Error: ID and LANGUAGE_TAG are required"; \
		exit 1; \
	fi
	poetry run youversion add-theme $(ID) --language-tag $(LANGUAGE_TAG)

cli-remove-theme:
	@echo "Usage: make cli-remove-theme ID=1"
	@if [ -z "$(ID)" ]; then \
		echo "Error: ID is required"; \
		exit 1; \
	fi
	poetry run youversion remove-theme $(ID)

cli-set-theme:
	@echo "Usage: make cli-set-theme ID=1"
	@if [ -z "$(ID)" ]; then \
		echo "Error: ID is required"; \
		exit 1; \
	fi
	poetry run youversion set-theme $(ID)

cli-get-theme-description:
	@echo "Usage: make cli-get-theme-description ID=1 LANGUAGE_TAG='eng'"
	@if [ -z "$(ID)" ] || [ -z "$(LANGUAGE_TAG)" ]; then \
		echo "Error: ID and LANGUAGE_TAG are required"; \
		exit 1; \
	fi
	poetry run youversion get-theme-description $(ID) --language-tag $(LANGUAGE_TAG)

cli-send-friend-request:
	@echo "Usage: make cli-send-friend-request USER_ID=123456"
	@if [ -z "$(USER_ID)" ]; then \
		echo "Error: USER_ID is required"; \
		exit 1; \
	fi
	poetry run youversion send-friend-request $(USER_ID)

cli-get-localization-items:
	poetry run youversion get-localization-items


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

