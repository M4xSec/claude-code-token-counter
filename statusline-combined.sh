#!/bin/bash
export LANG=en_US.UTF-8
export LC_ALL=en_US.UTF-8
export PYTHONIOENCODING=utf-8
INPUT=$(cat)

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BARS=$(echo "$INPUT" | python3 "$SCRIPT_DIR/claude-counter-statusline.py" 2>/dev/null)

if [ -n "$BARS" ]; then
    echo "$BARS"
fi
