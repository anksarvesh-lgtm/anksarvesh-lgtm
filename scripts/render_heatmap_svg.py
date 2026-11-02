"""Render data/contributions.json as an animated 53x7 heatmap SVG.

With no data file it renders an empty grid, so the profile never shows a broken image.
"""
import json, os
from datetime import date, timedelta

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data", "contributions.json")
OUT = os.path.join(ROOT, "contrib-heatmap.svg")
PALETTE = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353", "#69f0a0"]
BOX, GAP = 13, 3
PITCH = BOX + GAP
X0, Y0 = 44, 38


def load():
    if os.path.exists(DATA):
        d = json.load(open(DATA))
        return d["days"], d["stats"], True
    end = date.today()
    days = [{"date": (end - timedelta(days=i)).isoformat(), "count": 0, "level": 0}
            for i in range(370, -1, -1)]
    return days, None, False


def main():
    days, st, live = load()
    first = date.fromisoformat(days[0]["date"])
    offset = (first.weekday() + 1) % 7  # GitHub weeks start on Sunday
    cells, months = [], []
    last_month = None
    for i, d in enumerate(days):
        idx = i + offset
        wk, dow = divmod(idx, 7)
        dt = date.fromisoformat(d["date"])
        lvl = min(int(d["level"]), 5)
        x, y = X0 + wk * PITCH, Y0 + dow * PITCH
        delay = round((wk + dow) * 0.012, 3)
        tip = f'{d["count"]} contributions on {d["date"]}'
        cells.append(f'<rect class="c" style="animation-delay:{delay}s" x="{x}" y="{y}" '
                     f'width="{BOX}" height="{BOX}" rx="3" fill="{PALETTE[lvl]}"><title>{tip}</title></rect>')
        if dt.month != last_month and dt.day <= 7 and dow == 0 or last_month is None:
            if not months or x - months[-1][0] >= 44:
                months.append((x, dt.strftime("%b")))
            last_month = dt.month
    width = X0 + 53 * PITCH + 20
    mlabels = "".join(f'<text x="{x}" y="28" class="t">{m}</text>' for x, m in months)
    dlabels = "".join(f'<text x="10" y="{Y0 + r * PITCH + 11}" class="t">{n}</text>'
                      for r, n in ((1, "Mon"), (3, "Wed"), (5, "Fri")))
    ly = Y0 + 7 * PITCH + 18
    legend = "".join(f'<rect x="{width - 190 + i * 18}" y="{ly - 11}" width="13" height="13" rx="3" fill="{c}"/>'
                     for i, c in enumerate(PALETTE))
    if live:
        foot = (f'{st["total"]:,} contributions in the last year  ·  current streak {st["current_streak"]}d'
                f'  ·  longest streak {st["longest_streak"]}d')
    else:
        foot = "contribution graph refreshes daily with GitHub Actions"
    height = ly + 28
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}" role="img" aria-label="GitHub contribution heatmap">
<style>
.t{{font:11px ui-monospace,Menlo,Consolas,monospace;fill:#8b949e}}
.f{{font:12px ui-monospace,Menlo,Consolas,monospace;fill:#c9d1d9}}
.c{{animation:pop .45s ease-out both}}
@keyframes pop{{from{{opacity:0;transform:translateY(-8px)}}to{{opacity:1;transform:translateY(0)}}}}
</style>
<rect width="{width}" height="{height}" rx="12" fill="#0d1117" stroke="#30363d"/>
{mlabels}{dlabels}
{"".join(cells)}
<text x="{X0}" y="{ly}" class="f">{foot}</text>
<text x="{width - 220}" y="{ly}" class="t" text-anchor="end">Less</text>
{legend}
<text x="{width - 78}" y="{ly}" class="t">More</text>
</svg>'''
    open(OUT, "w", encoding="utf-8").write(svg)
    print("wrote", OUT, "live" if live else "empty-state")


if __name__ == "__main__":
    main()
