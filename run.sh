#!/bin/bash

# Resume Project Runner with WeasyPrint Support
# This script sets up the proper environment for WeasyPrint to work on macOS

# Set up library paths for WeasyPrint
export DYLD_LIBRARY_PATH="/opt/homebrew/lib:$DYLD_LIBRARY_PATH"
export PKG_CONFIG_PATH="/opt/homebrew/lib/pkgconfig"
export PATH="$HOME/.local/bin:$PATH"

# Function to show usage
usage() {
    echo "Usage: $0 [command]"
    echo ""
    echo "Commands:"
    echo "  dev         - Start Flask development server"
    echo "  build       - Generate static files (original layout)"
    echo "  build-cols  - Generate column-based PDF"
    echo "  sync        - Install/sync dependencies"
    echo "  shell       - Open shell with proper environment"
    echo ""
    echo "Examples:"
    echo "  $0 dev         # Start development server"
    echo "  $0 build       # Generate original static site"

}

# Execute based on command
case "${1:-help}" in
    "dev"|"serve")
        echo "🚀 Starting Flask development server..."
        uv run python -m flask run
        ;;
    "build"|"static")
        echo "📦 Generating static files..."
        uv run python gen_static.py
        echo "✅ Static files generated in docs/"
        ;;
    
    "sync"|"install")
        echo "📥 Syncing dependencies..."
        uv sync
        ;;
    "shell")
        echo "🐚 Opening shell with proper environment..."
        exec $SHELL
        ;;
    "help"|*)
        usage
        ;;
esac
