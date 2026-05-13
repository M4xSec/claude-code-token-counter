#!/bin/bash
set -e

INSTALL_DIR="$HOME/.claude"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "Installing Claude Code Token Counter statusline plugin..."

# Create install directory if it doesn't exist
mkdir -p "$INSTALL_DIR"

# Copy plugin files
cp "$SCRIPT_DIR/claude-counter-statusline.py" "$INSTALL_DIR/"
cp "$SCRIPT_DIR/statusline-combined.sh" "$INSTALL_DIR/"

# Make scripts executable
chmod +x "$INSTALL_DIR/claude-counter-statusline.py"
chmod +x "$INSTALL_DIR/statusline-combined.sh"

# Configure settings.json
SETTINGS_FILE="$INSTALL_DIR/settings.json"

if [ -f "$SETTINGS_FILE" ]; then
    # Backup existing settings
    cp "$SETTINGS_FILE" "$SETTINGS_FILE.bak"
    echo "Backed up existing settings to $SETTINGS_FILE.bak"

    # Check if statusLine is already configured
    if python3 -c "
import json, sys
with open('$SETTINGS_FILE') as f:
    d = json.load(f)
if 'statusLine' in d:
    sys.exit(0)
sys.exit(1)
" 2>/dev/null; then
        echo "statusLine already configured in settings.json — updating command path..."
    fi

    # Update/add statusLine config
    python3 -c "
import json
with open('$SETTINGS_FILE') as f:
    d = json.load(f)
d['statusLine'] = {
    'type': 'command',
    'command': '$INSTALL_DIR/statusline-combined.sh',
    'refreshInterval': 30
}
with open('$SETTINGS_FILE', 'w') as f:
    json.dump(d, f, indent=2)
print('Updated settings.json with statusLine config')
"
else
    # Create new settings.json with statusLine config
    python3 -c "
import json
d = {
    'statusLine': {
        'type': 'command',
        'command': '$INSTALL_DIR/statusline-combined.sh',
        'refreshInterval': 30
    }
}
with open('$SETTINGS_FILE', 'w') as f:
    json.dump(d, f, indent=2)
print('Created settings.json with statusLine config')
"
fi

echo ""
echo "Installation complete!"
echo "Restart Claude Code to see the token counter in your status line."
echo ""
echo "The status line shows:"
echo "  • 5h  — 5-hour rate limit usage (with reset countdown)"
echo "  • 7d  — 7-day rate limit usage (with reset countdown)"
echo "  • ctx — Context window usage (with token count)"
