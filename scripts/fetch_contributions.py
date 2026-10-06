"""Fetch the public contribution calendar (no token needed) -> data/contributions.json."""
import json
import os
import re
import sys
from pathlib import Path

import requests
from bs4 import BeautifulSoup

USER = os.environ.get("GITHUB_USER") or (sys.argv[1] if len(sys.argv) > 1 else "Przz23")
OUT = Path(__file__).resolve().parent.parent / "data" / "contributions.json"


def main() -> None:
    r = requests.get(
        f"https://github.com/users/{USER}/contributions",
        headers={"User-Agent": "Mozilla/5.0 (profile-readme-bot)"},
        timeout=30,
    )
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")

    counts = {}
    for tip in soup.find_all("tool-tip"):
        m = re.match(r"(\d+) contributions?", tip.get_text(strip=True))
        counts[tip.get("for")] = int(m.group(1)) if m else 0

    days = []
    for td in soup.select("td.ContributionCalendar-day[data-date]"):
        days.append(
            {
                "date": td["data-date"],
                "count": counts.get(td.get("id"), 0),
                "level": int(td.get("data-level", 0)),
            }
        )
    if not days:
        sys.exit("No contribution cells found; GitHub markup may have changed.")
    days.sort(key=lambda d: d["date"])

    # No timestamp on purpose: the file only changes when the data does,
    # so the workflow commits only when there is something new.
    data = {"user": USER, "total": sum(d["count"] for d in days), "days": days}
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(data, indent=1) + "\n", encoding="utf-8")
    print(f"{len(days)} days, {data['total']} contributions -> {OUT}")


if __name__ == "__main__":
    main()
