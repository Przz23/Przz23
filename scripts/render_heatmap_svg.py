"""data/contributions.json -> contrib-heatmap.svg (diagonal reveal, plays once)."""
import json
from datetime import date, timedelta
from pathlib import Path

from theme import ACCENT, BG, BORDER, FONT, HEAT, MUTED, TEXT, title_bar

ROOT = Path(__file__).resolve().parent.parent
W, CELL, PITCH, X0, Y0 = 860, 12, 15, 52, 100
MONTHS = "Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split()
PROMPT = "git log --author=przz23 --since='1 year ago' --stat"


def streaks(days):
    longest = cur = 0
    for d in days:
        cur = cur + 1 if d["count"] else 0
        longest = max(longest, cur)
    current = 0
    for i, d in enumerate(reversed(days)):
        if d["count"]:
            current += 1
        elif i == 0:
            continue  # today may still be empty
        else:
            break
    return longest, current


def main() -> None:
    data = json.loads((ROOT / "data" / "contributions.json").read_text(encoding="utf-8"))
    days = data["days"]
    first = date.fromisoformat(days[0]["date"])
    start = first - timedelta(days=(first.weekday() + 1) % 7)  # back to Sunday

    cells, months, last_month = [], [], None
    for d in days:
        dt = date.fromisoformat(d["date"])
        col, row = (dt - start).days // 7, (dt.weekday() + 1) % 7
        x, y = X0 + col * PITCH, Y0 + row * PITCH
        delay = 0.6 + col * 0.018 + row * 0.04
        cells.append(
            f'<rect class="c" x="{x}" y="{y}" width="{CELL}" height="{CELL}" rx="2" '
            f'fill="{HEAT[min(d["level"], 5)]}" style="animation-delay:{delay:.2f}s"/>'
        )
        if dt.month != last_month:
            if not months or x - months[-1][0] >= 36:
                months.append((x, MONTHS[dt.month - 1]))
            last_month = dt.month

    longest, current = streaks(days)
    best = max(days, key=lambda d: d["count"])
    foot_y = Y0 + 7 * PITCH + 34
    H = foot_y + 26

    month_txt = "".join(
        f'<text class="f" x="{x}" y="{Y0 - 8}" font-size="10" fill="{MUTED}">{m}</text>' for x, m in months
    )
    wd_txt = "".join(
        f'<text class="f" x="{X0 - 10}" y="{Y0 + r * PITCH + 10}" text-anchor="end" font-size="10" fill="{MUTED}">{n}</text>'
        for r, n in ((1, "Mon"), (3, "Wed"), (5, "Fri"))
    )
    lx = W - 20 - 6 * PITCH - 66
    legend = (
        f'<text class="f" x="{lx}" y="{foot_y}" text-anchor="end" font-size="10" fill="{MUTED}">less</text>'
        + "".join(
            f'<rect class="f" x="{lx + 8 + i * PITCH}" y="{foot_y - 10}" width="{CELL}" height="{CELL}" rx="2" fill="{c}"/>'
            for i, c in enumerate(HEAT)
        )
        + f'<text class="f" x="{lx + 14 + 6 * PITCH}" y="{foot_y}" font-size="10" fill="{MUTED}">more</text>'
    )
    stats = (
        f'<text class="f" x="{X0}" y="{foot_y}" font-size="12" fill="{TEXT}">'
        f'<tspan fill="{ACCENT}">{data["total"]}</tspan> contributions · '
        f'longest streak <tspan fill="{ACCENT}">{longest}d</tspan> · '
        f'current <tspan fill="{ACCENT}">{current}d</tspan> · '
        f'best day <tspan fill="{ACCENT}">{best["count"]}</tspan></text>'
    )
    prompt_w = round((len(PROMPT) + 2) * 7.5)

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="GitHub contribution heatmap, last year">
<style>
text{{font-family:{FONT}}}
.c{{opacity:0;transform-box:fill-box;transform-origin:center;animation:pop .35s ease-out forwards}}
.f{{opacity:0;animation:fade .6s ease-out 1.4s forwards}}
@keyframes pop{{from{{opacity:0;transform:scale(.4)}}to{{opacity:1;transform:scale(1)}}}}
@keyframes fade{{to{{opacity:1}}}}
@media (prefers-reduced-motion:reduce){{.c,.f{{animation:none;opacity:1}}}}
</style>
<defs><clipPath id="pc"><rect x="{X0}" y="46" width="0" height="22"><animate attributeName="width" from="0" to="{prompt_w}" dur="1s" begin="0.1s" fill="freeze"/></rect></clipPath></defs>
<rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="8" fill="{BG}" stroke="{BORDER}"/>
{title_bar(W, "przz23 — contributions")}
<g clip-path="url(#pc)"><text x="{X0}" y="62" font-size="12.5" fill="{TEXT}" xml:space="preserve"><tspan fill="{ACCENT}">$ </tspan>{PROMPT.replace("'", "&#39;")}</text></g>
{month_txt}{wd_txt}
{"".join(cells)}
{stats}{legend}
</svg>
'''
    out = ROOT / "contrib-heatmap.svg"
    out.write_text(svg, encoding="utf-8")
    print(f"-> {out} ({len(days)} days)")


if __name__ == "__main__":
    main()
