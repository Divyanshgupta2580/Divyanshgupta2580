"""Refresh the language tables in the GitHub profile README."""

import json
import os
import re
from datetime import datetime
from html import escape
from pathlib import Path
from time import sleep
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen
from zoneinfo import ZoneInfo


README = Path(__file__).resolve().parents[2] / "README.md"
API_URL = "https://api.wakatime.com/api/v1/users/current/stats"
RANGES = ("last_7_days", "last_30_days", "last_year")
LANGUAGE_LIMIT = 5


def fetch_stats(time_range, token):
    request = Request(
        f"{API_URL}/{time_range}",
        headers={"Authorization": f"Bearer {token}", "Accept": "application/json"},
    )
    for delay in (0, 10, 30, 60):
        sleep(delay)
        try:
            with urlopen(request, timeout=15) as response:
                if response.status == 202:
                    continue
                stats = json.load(response)["data"]
                if stats["is_up_to_date"]:
                    return stats
        except HTTPError as error:
            message = f"WakaTime returned HTTP {error.code} for {time_range}."
            if error.code in (401, 403):
                message += " Check that WAKATIME_API_KEY contains a WakaTime OAuth token with stats access."
            raise RuntimeError(message) from None
        except (URLError, TimeoutError):
            raise RuntimeError(f"Could not reach WakaTime for {time_range}.") from None

    print(f"::warning::WakaTime is still calculating {time_range}. Keeping the existing section.")
    return None


def format_duration(seconds):
    hours, minutes = divmod(int(seconds // 60), 60)
    if hours:
        return f"{hours}h {minutes:02d}m"
    return f"{minutes}m" if minutes else "<1m"


def format_stats(stats):
    languages = [
        (entry["name"], entry["total_seconds"])
        for entry in stats["languages"]
        if entry["name"] != "Other" and entry["total_seconds"] > 0
    ]
    languages.sort(key=lambda entry: (-entry[1], entry[0]))
    end = datetime.fromisoformat(stats["end"]).astimezone(ZoneInfo(stats["timezone"]))
    through = f"through {end:%b %d, %Y}"
    if not languages:
        return f"_No language activity recorded {through}._"

    total_seconds = sum(seconds for _, seconds in languages)
    rows = [
        f"**{format_duration(total_seconds)}** tracked · {through}",
        "",
        "| Language | Time | Share |",
        "| :--- | ---: | :--- |",
    ]
    for name, seconds in languages[:LANGUAGE_LIMIT]:
        name = " ".join(name.split())
        label = re.sub(r"([\\`*_\[\]~|])", r"\\\1", escape(name))
        share = 100 * seconds / total_seconds
        filled = round(share / 10)
        bar = "█" * filled + "░" * (10 - filled)
        rows.append(f"| {label} | `{format_duration(seconds)}` | `{bar} {share:.1f}%` |")
    return "\n".join(rows)


def split_section(content, section):
    start = f"<!--START_SECTION:{section}-->"
    end = f"<!--END_SECTION:{section}-->"
    if content.count(start) != 1 or content.count(end) != 1 or content.index(start) > content.index(end):
        raise RuntimeError(f"README.md needs one ordered pair of markers for {section}.")
    before, _, rest = content.partition(start)
    body, _, after = rest.partition(end)
    return before + start, body, end + after


def main():
    token = os.environ.get("WAKATIME_OAUTH_TOKEN", "").strip()
    if not token:
        raise RuntimeError("Set the WAKATIME_API_KEY Actions secret to your WakaTime OAuth token.")

    original = README.read_text(encoding="utf-8")
    before, section, after = split_section(original, "waka")
    for time_range in RANGES:
        marker = f"waka-{time_range}"
        prefix, _, suffix = split_section(section, marker)
        try:
            stats = fetch_stats(time_range, token)
            if stats is not None:
                section = f"{prefix}\n\n{format_stats(stats)}\n\n{suffix}"
        except (KeyError, TypeError, ValueError):
            raise RuntimeError(f"WakaTime returned unexpected stats for {time_range}.") from None

    updated = before + section + after
    if original != updated:
        README.write_text(updated, encoding="utf-8")


if __name__ == "__main__":
    try:
        main()
    except RuntimeError as error:
        raise SystemExit(str(error)) from None
