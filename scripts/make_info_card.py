"""Hand-authored neofetch-style info card. Edit ROWS, then run: python scripts/make_info_card.py"""
import os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W, H = 490, 397
ROWS = [
    ("Role", "Agriculturist · Founder · Developer"),
    ("Education", "M.Sc. Horticulture, DDU Gorakhpur (2025)"),
    ("Now", "Agrigence journal + exam prep app"),
    ("Consulting", "Fivearth Farms, organic (Alwar)"),
    ("Standards", "NPOP · USDA · EU"),
    ("Exams", "IBPS AFO, ICAR JRF, UPSSSC AGTA, PSC"),
    ("Stack", "React · Node · Firebase · TS · Python · Swift"),
    ("App", "Agrigence on Google Play"),
    ("Web", "agrigence.in"),
    ("Based", "India"),
]
BLOCKS = ["#ff5f56", "#ffbd2e", "#27c93f", "#39d353", "#69f0a0", "#7dd3fc", "#fde68a", "#f9a8d4"]


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;")


def main():
    out, delay = [], 0.2
    out.append(f'<text x="24" y="66" class="p" style="animation-delay:{delay}s"><tspan class="g">sarvesh@agrigence</tspan><tspan class="d">:~$ </tspan>neofetch</text>')
    delay += 0.5
    out.append(f'<text x="24" y="98" class="n" style="animation-delay:{delay}s">Sarvesh Yadav</text>')
    out.append(f'<text x="24" y="110" class="d" style="animation-delay:{delay}s">{"─" * 46}</text>')
    y = 136
    for k, v in ROWS:
        delay += 0.22
        out.append(f'<text x="24" y="{y}" class="r" style="animation-delay:{delay:.2f}s"><tspan class="k">{esc(k)}</tspan>'
                   f'<tspan x="120" class="v">{esc(v)}</tspan></text>')
        y += 20
    delay += 0.25
    blocks = "".join(f'<rect x="{24 + i * 26}" y="{y + 2}" width="22" height="14" rx="3" fill="{c}"/>' for i, c in enumerate(BLOCKS))
    out.append(f'<g class="r" style="animation-delay:{delay:.2f}s">{blocks}</g>')
    out.append(f'<text x="24" y="{y + 42}" class="p" style="animation-delay:{delay + .3:.2f}s"><tspan class="g">sarvesh@agrigence</tspan><tspan class="d">:~$ </tspan><tspan class="cur">█</tspan></text>')
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Sarvesh Yadav: agriculturist, founder, developer">
<style>
text{{font:13px ui-monospace,Menlo,Consolas,monospace;fill:#e6edf3}}
.g{{fill:#86efac}} .d{{fill:#8b949e}} .k{{fill:#86efac;font-weight:700}} .v{{fill:#e6edf3}}
.n{{font-size:20px;font-weight:800;fill:#ffffff}}
.p,.r,.n{{animation:in .5s ease-out both}}
.cur{{animation:blink 1s steps(2,end) infinite}}
@keyframes in{{from{{opacity:0;transform:translateX(-8px)}}to{{opacity:1;transform:translateX(0)}}}}
@keyframes blink{{50%{{opacity:0}}}}
</style>
<rect width="{W}" height="{H}" rx="12" fill="#0d1117" stroke="#30363d"/>
<circle cx="20" cy="16" r="5" fill="#ff5f56"/><circle cx="38" cy="16" r="5" fill="#ffbd2e"/><circle cx="56" cy="16" r="5" fill="#27c93f"/>
<text x="{W - 14}" y="20" text-anchor="end" style="fill:#8b949e;font-size:12px">info.sh</text>
{"".join(out)}
</svg>'''
    open(os.path.join(ROOT, "info-card.svg"), "w", encoding="utf-8").write(svg)
    print("wrote info-card.svg")


if __name__ == "__main__":
    main()
