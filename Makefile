.PHONY: help dev build test clean install

# Default target
.DEFAULT_GOAL := help

# Environment variables for WeasyPrint on macOS
export DYLD_LIBRARY_PATH := /opt/homebrew/lib:$(DYLD_LIBRARY_PATH)
export PKG_CONFIG_PATH := /opt/homebrew/lib/pkgconfig
export PATH := $(HOME)/.local/bin:$(PATH)

help: ## Show this help message
	@echo "📄 Resume Project - Available Commands:"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-12s\033[0m %s\n", $$1, $$2}'
	@echo ""

dev: ## Start Flask development server on port 8080
	@echo "🚀 Starting Flask development server..."
	FLASK_RUN_PORT=8080 uv run python -m flask run

build: ## Generate static files for GitHub Pages
	@echo "📦 Generating static files..."
	@uv run python gen_static.py
	@echo "✅ Static files generated in docs/"

test: build ## Run tests (check PDF page counts)
	@echo "🧪 Running tests..."
	@python test_pdf_pages.py

install: ## Install/sync dependencies with uv
	@echo "📥 Syncing dependencies..."
	@uv sync

clean: ## Clean generated files
	@echo "🧹 Cleaning generated files..."
	@rm -rf docs/*.html docs/*.css docs/*.pdf
	@echo "✅ Cleaned"

check: ## Check that everything is set up correctly
	@echo "🔍 Checking setup..."
	@command -v uv >/dev/null 2>&1 || { echo "❌ uv not found. Install from https://github.com/astral-sh/uv"; exit 1; }
	@echo "✅ uv found"
	@test -f luisfernandobarrera.resume.json || { echo "❌ resume.json not found"; exit 1; }
	@echo "✅ resume.json found"
	@echo "✅ All checks passed"

all: install build test ## Install deps, build, and test

