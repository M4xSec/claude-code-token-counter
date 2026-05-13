#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import sys
import os
import time

os.environ.setdefault("PYTHONIOENCODING", "utf-8")
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

RESET = "\033[0m"
DIM = "\033[2m"
BOLD = "\033[1m"
RED = "\033[31m"
YELLOW = "\033[33m"
GREEN = "\033[32m"
CYAN = "\033[36m"
MAGENTA = "\033[35m"
RED_BOLD = "\033[1;31m"
YELLOW_BOLD = "\033[1;33m"
GREEN_BOLD = "\033[1;32m"

FILL = "━"   # heavy horizontal
EMPTY = "─"  # light horizontal


def make_bar(pct, width=12):
    pct = max(0.0, min(100.0, pct))
    filled = int(round(pct / 100.0 * width))
    empty = width - filled

    if pct >= 95:
        fg = RED_BOLD
    elif pct >= 80:
        fg = YELLOW_BOLD
    elif pct >= 50:
        fg = YELLOW
    else:
        fg = GREEN

    bar_filled = FILL * filled
    bar_empty = EMPTY * empty

    return f"{fg}{bar_filled}{DIM}{bar_empty}{RESET}"


def format_countdown(reset_epoch):
    if not reset_epoch:
        return ""
    now = time.time()
    diff = reset_epoch - now
    if diff <= 0:
        return "now"
    total_s = int(diff)
    if total_s < 60:
        return f"{total_s}s"
    total_m = total_s // 60
    if total_m < 60:
        return f"{total_m}m"
    h = total_m // 60
    m = total_m % 60
    if h < 24:
        return f"{h}h{m:02d}m"
    d = h // 24
    rh = h % 24
    return f"{d}d{rh}h"


def nested_get(data, *paths):
    for path in paths:
        obj = data
        for key in path.split("."):
            if isinstance(obj, dict):
                obj = obj.get(key)
            else:
                obj = None
                break
        if obj is not None:
            return obj
    return None


def main():
    raw = sys.stdin.read().strip()
    if not raw:
        return

    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        return

    five_pct = nested_get(data, "rate_limits.five_hour.used_percentage",
                          "rate_limits.five_hour.percent_used",
                          "rate_limits.five_hour")
    five_reset = nested_get(data, "rate_limits.five_hour.resets_at")

    seven_pct = nested_get(data, "rate_limits.seven_day.used_percentage",
                           "rate_limits.seven_day.percent_used",
                           "rate_limits.seven_day")
    seven_reset = nested_get(data, "rate_limits.seven_day.resets_at")

    ctx_pct = nested_get(data, "context_window.used_percentage",
                         "context_window.current_usage")
    ctx_tokens = nested_get(data, "context_window.total_input_tokens",
                            "context_window.current_tokens")

    has_limits = five_pct is not None or seven_pct is not None

    if not has_limits and ctx_pct is None:
        return

    parts = []

    if five_pct is not None:
        pct_val = float(five_pct)
        pct_str = f"{pct_val:.0f}" if pct_val == int(pct_val) else f"{pct_val:.1f}"
        countdown = format_countdown(five_reset)
        reset_str = f" {DIM}{countdown}{RESET}" if countdown else ""
        bar = make_bar(pct_val, 10)
        parts.append(f"{CYAN}5h{RESET} {bar} {BOLD}{pct_str}%{RESET}{reset_str}")

    if seven_pct is not None:
        pct_val = float(seven_pct)
        pct_str = f"{pct_val:.0f}" if pct_val == int(pct_val) else f"{pct_val:.1f}"
        countdown = format_countdown(seven_reset)
        reset_str = f" {DIM}{countdown}{RESET}" if countdown else ""
        bar = make_bar(pct_val, 10)
        parts.append(f"{MAGENTA}7d{RESET} {bar} {BOLD}{pct_str}%{RESET}{reset_str}")

    if ctx_pct is not None:
        cpct = float(ctx_pct)
        ctx_label = ""
        if ctx_tokens is not None:
            tk = int(ctx_tokens)
            if tk >= 1000000:
                ctx_label = f" {tk/1000000:.1f}M"
            elif tk >= 1000:
                ctx_label = f" {tk//1000}k"
        bar = make_bar(cpct, 6)
        parts.append(f"{DIM}ctx{RESET} {bar} {cpct:.0f}%{ctx_label}")

    if parts:
        print("  ".join(parts))


if __name__ == "__main__":
    main()
