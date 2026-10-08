#!/usr/bin/env python3
"""
Updates the WakaTime stats in README.md between:
<!--START_SECTION:waka-->
<!--END_SECTION:waka-->

Includes total active time, languages breakdown, and editors/IDEs breakdown.
Handles API errors gracefully without exposing secrets or failing builds.
"""

import os
import sys
import json
import base64
import urllib.request
import urllib.error
import configparser

def get_api_key():
    # 1. Environment variable (GitHub Actions)
    key = os.environ.get("WAKATIME_API_KEY", "").strip()
    if key:
        return key

    # 2. Local ~/.wakatime.cfg fallback (for local development/testing)
    cfg_path = os.path.expanduser("~/.wakatime.cfg")
    if os.path.exists(cfg_path):
        try:
            config = configparser.ConfigParser()
            config.read(cfg_path)
            local_key = config.get("settings", "api_key", fallback="").strip()
            if local_key:
                return local_key
        except Exception:
            pass

    return None

def make_bar(percent, bar_len=25):
    filled = int(round((percent / 100.0) * bar_len))
    filled = max(0, min(bar_len, filled))
    empty = bar_len - filled
    return "█" * filled + "░" * empty

def format_stats(data):
    total_time = data.get("human_readable_total", "")
    languages = data.get("languages", [])
    editors = data.get("editors", [])

    lines = []
    if total_time:
        lines.append(f"Total Active Time (Last 7 Days): {total_time}")
        lines.append("")

    # Filter out empty or negligible items
    filtered_langs = [l for l in languages if l.get("percent", 0) >= 1.0][:6]
    if filtered_langs:
        lines.append("Languages:")
        max_name_len = max(len(l.get("name", "")) for l in filtered_langs)
        max_time_len = max(len(l.get("text", "")) for l in filtered_langs)
        for l in filtered_langs:
            name = l.get("name", "").ljust(max(max_name_len, 14))
            time_text = l.get("text", "").ljust(max(max_time_len, 12))
            pct = l.get("percent", 0.0)
            bar = make_bar(pct, 25)
            lines.append(f"{name} {time_text} {bar}   {pct:05.2f} %")
        lines.append("")

    filtered_editors = [e for e in editors if e.get("percent", 0) >= 0.5][:5]
    if filtered_editors:
        lines.append("Editors & Tools:")
        max_ed_len = max(len(e.get("name", "")) for e in filtered_editors)
        max_ed_time_len = max(len(e.get("text", "")) for e in filtered_editors)
        for e in filtered_editors:
            name = e.get("name", "").ljust(max(max_ed_len, 15))
            time_text = e.get("text", "").ljust(max(max_ed_time_len, 12))
            pct = e.get("percent", 0.0)
            bar = make_bar(pct, 25)
            lines.append(f"{name} {time_text} {bar}   {pct:05.2f} %")

    return "\n".join(lines).strip()

def main():
    api_key = get_api_key()
    if not api_key:
        print("INFO: WAKATIME_API_KEY is not set. Preserving existing README content.")
        sys.exit(0)

    # Encode API key for Basic Auth
    auth_header = "Basic " + base64.b64encode(api_key.encode("utf-8")).decode("utf-8")
    url = "https://api.wakatime.com/api/v1/users/current/stats/last_7_days"
    req = urllib.request.Request(url, headers={"Authorization": auth_header})

    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            payload = json.loads(resp.read().decode("utf-8"))
            data = payload.get("data", {})
    except urllib.error.HTTPError as e:
        print(f"WARN: WakaTime API returned HTTP status {e.code}. Preserving existing content.")
        sys.exit(0)
    except Exception as e:
        print(f"WARN: Failed to connect to WakaTime API: {e}. Preserving existing content.")
        sys.exit(0)

    formatted_text = format_stats(data)
    if not formatted_text:
        print("INFO: No active WakaTime stats available for current period.")
        sys.exit(0)

    readme_path = "README.md"
    if not os.path.exists(readme_path):
        print("ERROR: README.md not found.")
        sys.exit(1)

    with open(readme_path, "r", encoding="utf-8") as f:
        content = f.read()

    start_marker = "<!--START_SECTION:waka-->"
    end_marker = "<!--END_SECTION:waka-->"

    start_idx = content.find(start_marker)
    end_idx = content.find(end_marker)

    if start_idx == -1 or end_idx == -1 or start_idx >= end_idx:
        print("ERROR: WakaTime section markers not found in README.md.")
        sys.exit(1)

    replacement = f"{start_marker}\n\n```txt\n{formatted_text}\n```\n\n{end_marker}"
    new_content = content[:start_idx] + replacement + content[end_idx + len(end_marker):]

    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(new_content)

    print("SUCCESS: Updated WakaTime statistics in README.md successfully.")

if __name__ == "__main__":
    main()
