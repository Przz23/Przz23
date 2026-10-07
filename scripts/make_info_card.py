"""Neofetch-style info card -> info-card-v2.svg. Set STATIC=1 for a frozen frame."""
import os
from pathlib import Path

from theme import ACCENT, BG, BORDER, FONT, MUTED, TEXT, esc, title_bar

ROOT = Path(__file__).resolve().parent.parent
STATIC = os.environ.get("STATIC") == "1"
W = 490

# (key, value) rows; None = blank spacer, str = section header
ROWS = [
    ("Role", "Telecommunications Engineering graduate"),
    ("University", "Universidad Miguel Hernández"),
    None,
    ("Interests", "Embedded Systems · Electronics"),
    ("", "Software Development · AI"),
    None,
    ("Languages", "C / C++ · Python · JavaScript"),
    ("Embedded", "ESP32 · STM32"),
    ("Web/Mobile", "Node.js · React Native · Supabase"),
    ("Tools", "MATLAB / Simulink · Git"),
    None,
    ("Projects", "Kira · Second Brain · GameHole · Koty"),
]


def main() -> None:
    lh, y = 22, 66
    out, i = [], 0

    def line(content: str, ypos: float) -> None:
        nonlocal i
        delay = 0.3 + i * 0.16
        style = "" if STATIC else f' style="animation-delay:{delay:.2f}s"'
        cls = "l s" if STATIC else "l"
        out.append(f'<g class="{cls}"{style}>{content}</g>')
        i += 1

    line(
        f'<text x="24" y="{y}" font-size="14" font-weight="700" fill="{ACCENT}">alejandro<tspan fill="{MUTED}">@</tspan>przz23</text>',
        y,
    )
    y += 8
    out.append(f'<rect x="24" y="{y}" width="{W - 48}" height="1" fill="{BORDER}"/>')
    y += lh
    for row in ROWS:
        if row is None:
            y += lh // 2
            continue
        k, v = row
        line(
            f'<text x="24" y="{y}" font-size="13" fill="{ACCENT}" xml:space="preserve">{esc(k)}</text>'
            f'<text x="130" y="{y}" font-size="13" fill="{TEXT}" xml:space="preserve">{esc(v)}</text>',
            y,
        )
        y += lh
    # colour swatches, like neofetch
    y += 6
    sw = "".join(
        f'<rect x="{24 + n * 22}" y="{y}" width="18" height="10" rx="2" fill="{c}"/>'
        for n, c in enumerate(["#161b22", "#0f3d2a", "#17694a", "#25a06a", "#3fd48a", "#69f0a0"])
    )
    line(sw, y)
    H = y + 28

    anim = "" if STATIC else (
        ".l{opacity:0;animation:in .5s ease-out forwards}"
        "@keyframes in{from{opacity:0;transform:translateX(-8px)}to{opacity:1;transform:none}}"
        "@media (prefers-reduced-motion:reduce){.l{animation:none;opacity:1}}"
    )
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Profile summary">
<style>text{{font-family:{FONT}}}.s{{opacity:1}}{anim}</style>
<rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="8" fill="{BG}" stroke="{BORDER}"/>
{title_bar(W, "alejandro@przz23: ~")}
{chr(10).join(out)}
</svg>
'''
    dest = ROOT / "info-card-v2.svg"
    dest.write_text(svg, encoding="utf-8")
    print(f"-> {dest} ({W}x{H})")


if __name__ == "__main__":
    main()
