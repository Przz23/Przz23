"""Prepare a photo for ASCII conversion.

    python scripts/prep_photo.py [input] [output]

Defaults: photo/source.jpg -> photo/processed.png   (the photo/ folder is git-ignored)

Steps: optional background removal (rembg) -> local contrast (OpenCV CLAHE, or Pillow
fallback) -> composite on white -> square-ish portrait crop.
"""
import sys
from pathlib import Path

from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parent.parent
SRC = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "photo" / "source.jpg"
DST = Path(sys.argv[2]) if len(sys.argv) > 2 else ROOT / "photo" / "processed.png"


def main() -> None:
    if not SRC.exists():
        sys.exit(f"Photo not found: {SRC}\nPut your photo there (it is git-ignored, never committed).")
    img = Image.open(SRC)
    img = ImageOps.exif_transpose(img).convert("RGBA")

    try:
        from rembg import remove  # optional

        img = remove(img)
        print("background removed (rembg)")
    except ImportError:
        print("rembg not installed: keeping original background (pip install rembg for best results)")

    white = Image.new("RGBA", img.size, (255, 255, 255, 255))
    gray = Image.alpha_composite(white, img).convert("L")

    try:
        import cv2
        import numpy as np

        clahe = cv2.createCLAHE(clipLimit=2.5, tileGridSize=(8, 8))
        gray = Image.fromarray(clahe.apply(np.array(gray)))
        print("contrast: CLAHE (OpenCV)")
    except ImportError:
        gray = ImageOps.autocontrast(gray, cutoff=1)
        print("contrast: autocontrast (Pillow)")

    # 4:5 portrait crop, centred
    w, h = gray.size
    tw = min(w, int(h * 0.8))
    th = int(tw * 1.25)
    left, top = (w - tw) // 2, max(0, (h - th) // 2)
    gray = gray.crop((left, top, left + tw, min(h, top + th)))

    DST.parent.mkdir(parents=True, exist_ok=True)
    gray.save(DST)
    print(f"-> {DST} {gray.size}")


if __name__ == "__main__":
    main()
