"""Fetch the public contribution calendar for a GitHub user (no token needed).

Writes data/contributions.json with the raw days plus streak/total stats.
"""
import json, os, re, sys
from datetime import date, timedelta

import requests
from bs4 import BeautifulSoup

USER = os.environ.get("GH_USER", "anksarvesh-lgtm")
URL = f"https://github.com/users/{USER}/contributions"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "data", "contributions.json")


def fetch_days():
    r = requests.get(URL, headers={"User-Agent": "profile-readme-bot"}, timeout=30)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")

    # tooltips hold the real counts: "3 contributions on June 4th." / "No contributions on ..."
    counts = {}
    for tip in soup.find_all("tool-tip"):
        target = tip.get("for")
        m = re.match(r"(\d+|No)\s+contribution", tip.get_text(strip=True))
        if target and m:
            counts[target] = 0 if m.group(1) == "No" else int(m.group(1))

    days = []
    for cell in soup.select("td[data-date]"):
        d = cell["data-date"]
        level = int(cell.get("data-level", 0))
        n = counts.get(cell.get("id"), None)
        if n is None:
            n = 0 if level == 0 else level  # fallback if tooltip missing
        days.append({"date": d, "count": n, "level": level})
    days.sort(key=lambda x: x["date"])
    return days


def stats(days):
    total = sum(d["count"] for d in days)
    best = max(days, key=lambda d: d["count"]) if days else None
    longest = cur = 0
    for d in days:
        cur = cur + 1 if d["count"] > 0 else 0
        longest = max(longest, cur)
    # current streak: allow today to be empty
    streak = 0
    for d in reversed(days):
        if d["count"] > 0:
            streak += 1
        elif d["date"] == date.today().isoformat():
            continue
        else:
            break
    return {"total": total, "current_streak": streak, "longest_streak": longest,
            "best_day": best}


def main():
    days = fetch_days()
    if not days:
        sys.exit("No contribution cells found - GitHub markup may have changed.")
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as f:
        json.dump({"user": USER, "days": days, "stats": stats(days)}, f, indent=1)
    print(f"{len(days)} days, {stats(days)['total']} contributions")


if __name__ == "__main__":
    main()
