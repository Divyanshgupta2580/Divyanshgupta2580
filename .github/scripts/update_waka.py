#!/usr/bin/env python3
"""
Updates the WakaTime stats in README.md between:
<!--START_SECTION:waka-->
<!--END_SECTION:waka-->

Includes:
- Today's coding time
- Monthly coding time
- Yearly & All-Time coding time
- Languages breakdown with progress bars
Excludes:
- Editors & Tools breakdown (strictly removed per user specification)

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

def fetch_json(url, auth_header, timeout=12):
    req = urllib.request.Request(url, headers={"Authorization": auth_header})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        print(f"WARN: Failed fetching {url}: {e}")
        return None

def make_bar(percent, bar_len=25):
    filled = int(round((percent / 100.0) * bar_len))
    filled = max(0, min(bar_len, filled))
    empty = bar_len - filled
    return "█" * filled + "░" * empty

def main():
    api_key = get_api_key()
    if not api_key:
        print("INFO: WAKATIME_API_KEY is not set. Preserving existing README content.")
        sys.exit(0)

    auth_header = "Basic " + base64.b64encode(api_key.encode("utf-8")).decode("utf-8")

    # 1. Fetch Today's time
    today_data = fetch_json("https://api.wakatime.com/api/v1/users/current/summaries?range=today", auth_header)
    today_text = None
    if today_data:
        today_text = today_data.get("cumulative_total", {}).get("text")

    # 2. Fetch Monthly time (this_month)
    month_data = fetch_json("https://api.wakatime.com/api/v1/users/current/summaries?range=this_month", auth_header)
    month_text = None
    if month_data:
        month_text = month_data.get("cumulative_total", {}).get("text")

    # 3. Fetch Yearly time (last_year)
    year_data = fetch_json("https://api.wakatime.com/api/v1/users/current/stats/last_year", auth_header)
    year_text = None
    if year_data:
        year_text = year_data.get("data", {}).get("human_readable_total")

    # 4. Fetch All-Time cumulative time
    all_time_data = fetch_json("https://api.wakatime.com/api/v1/users/current/all_time_since_today", auth_header)
    all_time_text = None
    if all_time_data:
        all_time_text = all_time_data.get("data", {}).get("text")
    if not all_time_text and year_data:
        all_time_text = year_data.get("data", {}).get("text")

    # 5. Fetch Languages breakdown
    stats_data = fetch_json("https://api.wakatime.com/api/v1/users/current/stats/last_7_days", auth_header)
    languages = []
    if stats_data:
        languages = stats_data.get("data", {}).get("languages", [])

    lines = []

    # Time Summary Section (Today, Monthly, Yearly / All-Time)
    lines.append("Coding Activity:")
    if today_text:
        lines.append(f"Today:          {today_text}")
    else:
        lines.append("Today:          0 mins")

    if month_text:
        lines.append(f"This Month:     {month_text}")

    if year_text and all_time_text:
        lines.append(f"This Year:      {year_text} (All Time: {all_time_text})")
    elif year_text:
        lines.append(f"This Year:      {year_text}")
    elif all_time_text:
        lines.append(f"All Time:       {all_time_text}")

    lines.append("")

    # Languages Section
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

    formatted_text = "\n".join(lines).strip()
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
