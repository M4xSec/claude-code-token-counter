#!/bin/bash
set -e

INSTALL_DIR="$HOME/.claude"
SETTINGS_FILE="$INSTALL_DIR/settings.json"

echo "Uninstalling Claude Code Token Counter statusline plugin..."

# Remove plugin files
rm -f "$INSTALL_DIR/claude-counter-statusline.py"
rm -f "$INSTALL_DIR/statusline-combined.sh"

# Remove statusLine from settings.json
if [ -f "$SETTINGS_FILE" ]; then
    python3 -c "
import json
with open('$SETTINGS_FILE') as f:
    d = json.load(f)
if 'statusLine' in d:
    del d['statusLine']
with open('$SETTINGS_FILE', 'w') as f:
    json.dump(d, f, indent=2)
print('Removed statusLine config from settings.json')
" 2>/dev/null || echo "Could not update settings.json — remove statusLine entry manually"
fi

echo "Uninstall complete. Restart Claude Code."
