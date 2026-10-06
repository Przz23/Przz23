"""Processed photo -> ascii-portrait.svg (rows are revealed left-to-right, once).

    python scripts/make_ascii_svg.py [input] [output]

Defaults: photo/processed.png -> ascii-portrait.svg
"""
import sys
from pathlib import Path

import numpy as np
from PIL import Image

from theme import BG, BORDER, FONT, TEXT, esc

ROOT = Path(__file__).resolve().parent.parent
SRC = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "photo" / "processed.png"
DST = Path(sys.argv[2]) if len(sys.argv) > 2 else ROOT / "ascii-portrait.svg"

RAMP = " .`:-=+*cs#%@"  # sparse -> dense
COLS, CW, RH = 100, 6, 10  # characters per row, char width, row pitch (px)
PAD = 14


def main() -> None:
    if not SRC.exists():
        sys.exit(f"Not found: {SRC}\nRun scripts/prep_photo.py first.")
    img = Image.open(SRC).convert("L")
    rows = round(COLS * img.height / img.width * (CW / RH))
    a = np.asarray(img.resize((COLS, rows), Image.LANCZOS), dtype=float) / 255.0

    lines = []
    for r in range(rows):
        s = ""
        for v in a[r]:
            s += " " if v > 0.97 else RAMP[int(v * (len(RAMP) - 1) + 0.5)]  # white = background
        lines.append(s.rstrip())

    W, H = COLS * CW + PAD * 2, rows * RH + PAD * 2
    defs, texts = [], []
    for r, s in enumerate(lines):
        if not s.strip():
            continue
        y = PAD + r * RH
        begin = 0.2 + r * 0.035
        defs.append(
            f'<clipPath id="r{r}"><rect x="{PAD}" y="{y}" width="0" height="{RH}">'
            f'<animate attributeName="width" from="0" to="{COLS * CW}" dur="0.5s" begin="{begin:.3f}s" fill="freeze"/>'
            f"</rect></clipPath>"
        )
        texts.append(
            f'<text x="{PAD}" y="{y + RH - 2}" clip-path="url(#r{r})" textLength="{len(s) * CW}" '
            f'lengthAdjust="spacing" xml:space="preserve">{esc(s)}</text>'
        )

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="ASCII portrait">
<style>text{{font-family:{FONT};font-size:{RH}px;fill:{TEXT};white-space:pre}}</style>
<defs>{"".join(defs)}</defs>
<rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="8" fill="{BG}" stroke="{BORDER}"/>
{"".join(texts)}
</svg>
'''
    DST.write_text(svg, encoding="utf-8")
    print(f"-> {DST} ({COLS}x{rows} chars, {W}x{H}px)")


if __name__ == "__main__":
    main()
