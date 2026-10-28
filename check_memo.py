"""Step 5: check that every number in the memos appears in the generated results.

Usage:  .venv/bin/python check_memo.py

Collects every number in each memo and looks for it among the numbers in results/*.md
(the files the analysis scripts write). Small integers (<= 10) and years are skipped.
A number that isn't found was typed by hand and has to be traced or removed.
This catches invented numbers; it can't prove a number is used in the right place,
so every claim is also checked by hand against the results files.
"""

import re
import sys
from pathlib import Path

MEMOS = ["memo_1page.md", "memo_3page.md"]
NUMBER = re.compile(r"\d+(?:,\d{3})*(?:\.\d+)?")  # commas only as thousands separators: "105, 88" is two numbers


def numbers(text):
    return set(NUMBER.findall(text))


def trivial(token):
    if "," in token or "." in token:
        return False
    value = int(token)
    return value <= 10 or 2000 <= value <= 2030  # small counts like "two", and years


def main():
    results_numbers = numbers(" ".join(p.read_text() for p in Path("results").glob("*.md")))
    all_found = True
    for memo in MEMOS:
        text = re.sub(r"\]\([^)]*\)", "]", Path(memo).read_text())  # drop image/link paths
        missing = sorted(n for n in numbers(text) if not trivial(n) and n not in results_numbers)
        print(f"{memo}: {'all numbers found in results/' if not missing else 'NOT FOUND: ' + ', '.join(missing)}")
        all_found = all_found and not missing
    sys.exit(0 if all_found else 1)


if __name__ == "__main__":
    main()
