#!/usr/bin/env python3
"""Restore the original Rumi Adventure gameplay/art and apply a restrained 16-bit-style presentation."""
from pathlib import Path
import shutil

root = Path("source/RumiAdventure2")
html_path = root / "index.html"
html = html_path.read_text(encoding="utf-8")

# Deliberately preserve the original drawHero(), drawEnemy(), bg(), controls,
# level logic, and rumi-world artwork. Only restyle the presentation.
replacements = [
    (
        '#game{display:block;width:100vw;height:100dvh;background:#17102c}',
        '#game{display:block;width:100vw;height:100dvh;background:#17102c;image-rendering:pixelated;filter:contrast(1.08) saturate(1.12)}'
    ),
    (
        '.panel{padding:10px;border:2px solid #a66cff;border-radius:12px;background:#160d29dd}',
        '.panel{padding:10px;border:3px solid #bd7aff;border-radius:0;background:#160d29}'
    ),
    (
        '.bar{width:150px;max-width:35vw;height:13px;background:#3d263f;border:1px solid #fff6;border-radius:10px;overflow:hidden;margin-top:5px}',
        '.bar{width:150px;max-width:35vw;height:13px;background:#3d263f;border:2px solid #fff6;border-radius:0;overflow:hidden;margin-top:5px}'
    ),
    (
        '.fill{width:100%;height:100%;background:#ff4e83;transition:width .15s}',
        '.fill{width:100%;height:100%;background:#ff4e83;transition:width .15s;border-radius:0}'
    ),
    (
        'button{pointer-events:auto;touch-action:none;border:2px solid #d5aaff;background:#281747dd;color:white;border-radius:50%;width:65px;height:65px;font-size:25px;font-weight:bold;box-shadow:0 4px 0 #100a20}',
        'button{pointer-events:auto;touch-action:none;border:3px solid #e4b7ff;background:#281747;color:white;border-radius:0;width:65px;height:65px;font-size:25px;font-weight:bold;box-shadow:0 4px 0 #100a20;image-rendering:pixelated}'
    ),
    (
        '#restart{display:none;position:fixed;left:50%;top:57%;transform:translateX(-50%);border-radius:12px;',
        '#restart{display:none;position:fixed;left:50%;top:57%;transform:translateX(-50%);border-radius:0;'
    ),
    (
        '#startGame{border-radius:16px;width:auto;',
        '#startGame{border-radius:0;width:auto;'
    ),
    (
        '#intro img{position:absolute;width:100%;height:100%;object-fit:cover;inset:0;opacity:.92}',
        '#intro img{position:absolute;width:100%;height:100%;object-fit:cover;inset:0;opacity:.92;image-rendering:pixelated;filter:contrast(1.08) saturate(1.12)}'
    ),
    (
        'g.setTransform(D,0,0,D,0,0);floorY=',
        'g.setTransform(D,0,0,D,0,0);g.imageSmoothingEnabled=false;floorY='
    ),
]
for before, after in replacements:
    if before in html:
        html = html.replace(before, after)
    else:
        print("Note: style hook not present, skipped:", before[:70])

# Preserve all existing gameplay functions and assets; sync the HTML used by Android.
html_path.write_text(html, encoding="utf-8")
android_html = root / "android/app/src/main/assets/index.html"
android_html.parent.mkdir(parents=True, exist_ok=True)
shutil.copy2(html_path, android_html)

(root / "BUILD_16BIT.md").write_text(
    "Rumi Adventure — restrained 16-bit-style presentation\n\n"
    "This build restores the original game drawing and gameplay from the supplied source ZIP. "
    "The update changes the HUD/buttons to square pixel-era styling, applies crisp image rendering, "
    "and keeps the original Rumi world artwork, controls, enemies, and level logic.\n",
    encoding="utf-8"
)
print("Restored original gameplay/art and applied restrained 16-bit-style UI.")
