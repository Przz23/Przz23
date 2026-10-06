"""Shared palette and font stack for the profile SVGs (dark terminal look)."""

BG = "#0d1117"
BORDER = "#30363d"
TEXT = "#c9d1d9"
MUTED = "#8b949e"
ACCENT = "#69f0a0"
HEAT = ["#161b22", "#0f3d2a", "#17694a", "#25a06a", "#3fd48a", "#69f0a0"]
FONT = "ui-monospace, SFMono-Regular, Menlo, Consolas, 'Liberation Mono', monospace"


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def title_bar(width: int, label: str) -> str:
    """Fake terminal window chrome."""
    return (
        f'<rect x="0.5" y="0.5" width="{width - 1}" height="30" rx="8" fill="#161b22" stroke="{BORDER}"/>'
        '<circle cx="18" cy="16" r="5" fill="#ff5f56"/><circle cx="36" cy="16" r="5" fill="#ffbd2e"/>'
        '<circle cx="54" cy="16" r="5" fill="#27c93f"/>'
        f'<text x="{width / 2}" y="20" text-anchor="middle" font-size="12" fill="{MUTED}">{esc(label)}</text>'
    )
