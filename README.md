# Claude Code Token Counter

A status line plugin for [Claude Code](https://docs.anthropic.com/en/docs/claude-code) that displays real-time rate limit usage and context window stats directly in your terminal.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.6%2B-brightgreen)
![Platform](https://img.shields.io/badge/platform-linux%20%7C%20macOS-lightgrey)

---

## Preview

```
 5h ━━━━━━────── 58%  4h32m   7d ━━──────── 22%  6d14h   ctx ━━━─── 48% 125k
```

The status bar uses color-coded progress indicators:

| Color | Meaning |
|-------|---------|
| Green | Under 50% — plenty of headroom |
| Yellow | 50–80% — moderate usage |
| Bold Yellow | 80–95% — approaching limit |
| Bold Red | 95%+ — near capacity |

---

## What It Shows

| Indicator | Description |
|-----------|-------------|
| **5h** | 5-hour rolling rate limit usage + time until reset |
| **7d** | 7-day rolling rate limit usage + time until reset |
| **ctx** | Context window usage + total token count |

---

## Installation

### One-liner

```bash
git clone https://github.com/M4xSec/claude-code-token-counter.git && cd claude-code-token-counter && chmod +x install.sh && ./install.sh
```

### Step by step

```bash
git clone https://github.com/M4xSec/claude-code-token-counter.git
cd claude-code-token-counter
chmod +x install.sh
./install.sh
```

Restart Claude Code after installing.

### Manual

<details>
<summary>Click to expand manual installation steps</summary>

1. Copy files to `~/.claude/`:

```bash
mkdir -p ~/.claude
cp claude-counter-statusline.py ~/.claude/
cp statusline-combined.sh ~/.claude/
chmod +x ~/.claude/claude-counter-statusline.py
chmod +x ~/.claude/statusline-combined.sh
```

2. Add the `statusLine` block to `~/.claude/settings.json`:

```json
{
  "statusLine": {
    "type": "command",
    "command": "/home/YOUR_USER/.claude/statusline-combined.sh",
    "refreshInterval": 30
  }
}
```

Replace `/home/YOUR_USER` with your actual home path (`/Users/YOUR_USER` on macOS).

3. Restart Claude Code.

</details>

---

## Uninstall

```bash
chmod +x uninstall.sh
./uninstall.sh
```

---

## Configuration

The refresh interval controls how often the status line updates (in seconds):

```json
"refreshInterval": 15
```

| Value | Trade-off |
|-------|-----------|
| `15` | More responsive, slightly more overhead |
| `30` | Balanced (default) |
| `60` | Minimal overhead, less frequent updates |

---

## Requirements

- Claude Code CLI v1.0.24+
- Python 3.6+
- Bash

---

## How It Works

```
Claude Code                statusline-combined.sh         claude-counter-statusline.py
    │                              │                                │
    ├── pipes JSON status ──────►  │                                │
    │   (rate limits, context)     ├── forwards to python ────────► │
    │                              │                                ├── parses JSON
    │                              │                                ├── calculates bars
    │   ◄── ANSI-colored output ───┤  ◄── formatted string ────────┤
    │                              │                                │
```

Claude Code sends a JSON payload containing rate limit and context window data to the configured statusLine command on each refresh cycle. The shell wrapper passes it to the Python formatter, which outputs ANSI escape sequences for colored progress bars.

---

## File Structure

```
.
├── claude-counter-statusline.py   # Core formatter — parses JSON, outputs colored bars
├── statusline-combined.sh         # Bash wrapper — handles encoding, invokes Python
├── install.sh                     # Automated installer
├── uninstall.sh                   # Automated uninstaller
├── instructions.txt               # Plain-text install guide
└── README.md
```

---

## License

MIT
