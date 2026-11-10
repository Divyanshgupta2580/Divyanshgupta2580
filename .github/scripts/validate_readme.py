#!/usr/bin/env python3
"""Lightweight checks for the GitHub profile README."""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[2]
README = ROOT / "README.md"

REQUIRED_PROJECTS = ("BenefitOS", "TRON", "RevenueOS", "JanSetu Multiverse")
REQUIRED_SECTIONS = (
    "Selected Projects",
    "Technical Skills",
    "Areas of Focus",
    "GitHub Activity",
    "Coding Activity",
    "Problem Solving",
    "Contact",
)

def fail(message: str) -> None:
    print(f"FAIL: {message}")
    sys.exit(1)

def main() -> None:
    if not README.is_file():
        fail("README.md is missing")

    content = README.read_text(encoding="utf-8")

    for item in REQUIRED_PROJECTS:
        if item not in content:
            fail(f"Missing featured project: {item}")

    for section in REQUIRED_SECTIONS:
        if section not in content:
            fail(f"Missing section: {section}")

    if content.count("<!--START_SECTION:waka-->") != 1:
        fail("Expected exactly one WakaTime start marker")
    if content.count("<!--END_SECTION:waka-->") != 1:
        fail("Expected exactly one WakaTime end marker")

    if re.search(r"\b(first|second|third|final)[ -]year\b|\bstudent\b", content, re.I):
        fail("Student/year wording found in README")

    local_assets = re.findall(r"""(?:src)=["'](assets/[^"']+)["']""", content)
    for asset in local_assets:
        if not (ROOT / asset).is_file():
            fail(f"Missing local asset: {asset}")

    links = re.findall(r"""href=["'](https?://[^"']+)["']""", content)
    if not links:
        fail("No external links found")

    print("PASS: README structure, projects, markers, local assets, and profile wording validated.")
    print(f"Checked {len(links)} external links syntactically (not live network status).")

if __name__ == "__main__":
    main()
