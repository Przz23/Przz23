"""Animated projects card -> projects-card.svg. Set STATIC=1 for a frozen frame."""
import os
import textwrap
from pathlib import Path

from theme import ACCENT, BG, BORDER, FONT, MUTED, TEXT, esc, title_bar

ROOT = Path(__file__).resolve().parent.parent
STATIC = os.environ.get("STATIC") == "1"
W = 860
X = 28

# Generic descriptions only: the private projects are never described in detail.
PROJECTS = [
    {
        "name": "kira",
        "kind": "Embedded",
        "visibility": "public",
        "desc": "Autonomous voice-AI assistant robot on ESP32-S3: C firmware, I2S audio, round SPI display, custom PCB and 3D-printed body.",
        "stack": ["ESP32-S3", "C", "I2S", "SPI", "KiCad"],
        "link": "github.com/Przz23/kira",
    },
    {
        "name": "second-brain",
        "kind": "Desktop",
        "visibility": "public",
        "desc": "Local-first Windows app for notes, tasks, documents and project repos, with a private AI chat running locally on Qwen3 8B via Ollama. Installer on GitHub Releases.",
        "stack": ["Tauri", "Rust", "React", "SQLite", "Ollama"],
        "link": "github.com/Przz23/second-brain",
    },
    {
        "name": "gamehole",
        "kind": "Full-stack",
        "visibility": "private",
        "desc": "Full-stack web platform with authentication, payments, database and PWA support.",
        "stack": ["Node.js", "Supabase", "Stripe", "Vercel"],
    },
    {
        "name": "koty",
        "kind": "Mobile",
        "visibility": "private",
        "desc": "Cross-platform application with shared data, authentication and offline-oriented UX.",
        "stack": ["React Native", "Expo", "Supabase"],
    },
]


def chips(items, x, y):
    out = []
    for t in items:
        w = len(t) * 7.4 + 18
        out.append(
            f'<rect x="{x:.0f}" y="{y - 13}" width="{w:.0f}" height="20" rx="10" fill="#161b22" stroke="{BORDER}"/>'
            f'<text x="{x + w / 2:.0f}" y="{y + 1}" text-anchor="middle" font-size="11" fill="{TEXT}">{esc(t)}</text>'
        )
        x += w + 8
    return "".join(out)


def main() -> None:
    out, i, y = [], 0, 62

    def block(content: str) -> None:
        nonlocal i
        style = "" if STATIC else f' style="animation-delay:{0.3 + i * 0.45:.2f}s"'
        out.append(f'<g class="{"l s" if STATIC else "l"}"{style}>{content}</g>')
        i += 1

    block(f'<text x="{X}" y="{y}" font-size="13" fill="{TEXT}"><tspan fill="{ACCENT}">$ </tspan>ls -l ~/projects</text>')
    y += 34
    for p in PROJECTS:
        g = []
        g.append(f'<text x="{X}" y="{y}" font-size="15" font-weight="700" fill="{ACCENT}">{esc(p["name"])}</text>')
        nx = X + len(p["name"]) * 9 + 14
        g.append(f'<text x="{nx}" y="{y}" font-size="12" fill="{MUTED}">{esc(p["kind"])} · {p["visibility"]}</text>')
        if p.get("link"):
            g.append(f'<text x="{W - X}" y="{y}" text-anchor="end" font-size="12" fill="{MUTED}">{esc(p["link"])}</text>')
        y += 22
        for line in textwrap.wrap(p["desc"], 98):
            g.append(f'<text x="{X}" y="{y}" font-size="13" fill="{TEXT}">{esc(line)}</text>')
            y += 20
        y += 10
        g.append(chips(p["stack"], X, y))
        y += 26
        block("".join(g))
        out.append(f'<rect x="{X}" y="{y - 6}" width="{W - 2 * X}" height="1" fill="{BORDER}" class="{"s" if STATIC else "d"}"/>' if p is not PROJECTS[-1] else "")
        y += 22
    H = y - 4

    anim = "" if STATIC else (
        ".l,.d{opacity:0;animation:in .6s ease-out forwards}"
        "@keyframes in{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:none}}"
        "@media (prefers-reduced-motion:reduce){.l,.d{animation:none;opacity:1}}"
    )
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Projects">
<style>text{{font-family:{FONT}}}.s{{opacity:1}}{anim}</style>
<rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="8" fill="{BG}" stroke="{BORDER}"/>
{title_bar(W, "alejandro@przz23: ~/projects")}
{chr(10).join(out)}
</svg>
'''
    dest = ROOT / "projects-card.svg"
    dest.write_text(svg, encoding="utf-8")
    print(f"-> {dest} ({W}x{H})")


if __name__ == "__main__":
    main()
