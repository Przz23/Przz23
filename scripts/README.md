# Profile art

| File | Output | Runs |
|---|---|---|
| `fetch_contributions.py` | `data/contributions.json` | daily (GitHub Actions) |
| `render_heatmap_svg.py` | `contrib-heatmap.svg` | daily (GitHub Actions) |
| `make_info_card.py` | `info-card-v2.svg` | manually (`STATIC=1` for a frozen frame) |
| `prep_photo.py` + `make_ascii_svg.py` | `portrait.svg` | manually, locally |

## Add the ASCII portrait

1. Put your photo at `photo/source.jpg` (the `photo/` folder is git-ignored, the photo is never committed).
2. From the repo root:
   ```bash
   pip install -r scripts/requirements-photo.txt   # add rembg for background removal
   python scripts/prep_photo.py
   python scripts/make_ascii_svg.py
   ```
3. Review `portrait.svg`, then replace the `<img src="./info-card-v2.svg" ...>` block in `README.md` with:
   ```html
   <table>
     <tr>
       <td valign="top"><img src="./portrait.svg" alt="ASCII portrait" width="370"></td>
       <td valign="top"><img src="./info-card-v2.svg" alt="Profile summary" width="490"></td>
     </tr>
   </table>
   ```
4. Commit only `portrait.svg` and the README change.
