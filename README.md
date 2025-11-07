## Personal CV Building System ##

I'm fed up with the format of my CV and I decided to move all data to a JSON File with the [resume.json format](https://jsonresume.org/).

I adapted one of the themes and modified it to my needs using SASS, Jinja2 and Frozen Flask to template and generate static pages. It will read a file with `.resume.json` extension in the root file.

The CSS is optimized for screen and print.

## Quick Start

This project uses **uv** for dependency management and includes a **Makefile** for common tasks:

```bash
# See all available commands
make help

# Install dependencies
make install

# Start development server (port 8080)
make dev

# Generate static files for GitHub Pages
make build

# Run tests (verify PDF page counts)
make test

# Build and test everything
make all
```

### Alternative: Using run.sh or uv directly

```bash
# Using run.sh (legacy)
./run.sh dev
./run.sh build

# Using uv directly
uv sync
uv run python -m flask run
uv run python gen_static.py
```

## Templates Available

1. **Original Template** (`cv.html`) - Single-column web-optimized layout
2. **Column-Based Template** (`cv-columns.html`) - Professional two-column PDF-optimized layout

## Manual Commands

If you prefer to run commands manually:

```bash
# Install dependencies
uv sync

# Generate static files (requires environment setup)
export DYLD_LIBRARY_PATH="/opt/homebrew/lib:$DYLD_LIBRARY_PATH"
export PKG_CONFIG_PATH="/opt/homebrew/lib/pkgconfig"
uv run python gen_static.py

# Start development server
uv run python -m flask run 
```

## PDF Support

For PDF generation, you need:

1. **System dependencies** (automatically installed during setup):
   ```bash
   brew install gtk+3 gobject-introspection
   ```

2. **Fonts** (for optimal rendering):
   ```bash
   brew install font-merriweather font-source-sans-3 font-raleway
   ```

The `./run.sh build` command handles the environment setup automatically.

More info: [WeasyPrint Installation Guide](https://weasyprint.readthedocs.io/en/stable/install.html#gtk64installer)

Inside the `templates` folder you will find the template and the SASS file.

### TODO ###
- Mobile Template
