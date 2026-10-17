#!/usr/bin/env python3
"""Apply the first 16-bit visual pass to the existing Rumi Adventure HTML game."""
from pathlib import Path
import re
import shutil

root = Path("source/RumiAdventure2")
html_path = root / "index.html"
html = html_path.read_text(encoding="utf-8")

# Keep the existing gameplay, but make the interface look more like a pixel-art game.
html = html.replace(
    '#game{display:block;width:100vw;height:100dvh;background:#17102c}',
    '#game{display:block;width:100vw;height:100dvh;background:#17102c;image-rendering:pixelated}'
)
html = html.replace(
    '.panel{padding:10px;border:2px solid #a66cff;border-radius:12px;background:#160d29dd}',
    '.panel{padding:10px;border:3px solid #bd7aff;border-radius:0;background:#160d29}'
)
html = html.replace(
    'button{pointer-events:auto;touch-action:none;border:2px solid #d5aaff;background:#281747dd;color:white;border-radius:50%;width:65px;height:65px;font-size:25px;font-weight:bold;box-shadow:0 4px 0 #100a20}',
    'button{pointer-events:auto;touch-action:none;border:3px solid #e4b7ff;background:#281747;color:white;border-radius:0;width:65px;height:65px;font-size:25px;font-weight:bold;box-shadow:0 4px 0 #100a20;image-rendering:pixelated}'
)
html = html.replace(
    'g.setTransform(D,0,0,D,0,0);floorY=',
    'g.setTransform(D,0,0,D,0,0);g.imageSmoothingEnabled=false;floorY='
)

hero = r'''function drawHero(x,y){
  const moving=Math.abs(p.vx)>1&&!over;
  const stride=moving?Math.sin(t*14)*5:0;
  const arm=moving?Math.sin(t*14+Math.PI)*3:0;
  const bob=moving&&p.ground?Math.abs(Math.sin(t*14))*2:0;
  g.save();
  g.translate(Math.round(x),Math.round(y-bob));
  if(p.face<0){g.translate(p.w,0);g.scale(-1,1)}
  // Limited palette and hard-edged shapes create a chunky 16-bit look.
  const legA=moving?stride:0, legB=moving?-stride:0;
  g.fillStyle="#170d2b";
  g.fillRect(4+legA,31,9,10);g.fillRect(18+legB,31,9,10);
  g.fillStyle="#4b236f";
  g.fillRect(3+legA,39,11,4);g.fillRect(17+legB,39,12,4);
  g.fillStyle="#7134a8";g.fillRect(3,10,25,24);
  g.fillStyle="#9b4de0";g.fillRect(5,8,21,19);
  g.fillStyle="#c76cff";g.fillRect(5,3,22,13);
  g.fillStyle="#f2c8ff";g.fillRect(7,12,16,10);
  g.fillStyle="#3c1a69";g.fillRect(19,13,5,4);
  g.fillStyle="#ff6bba";g.fillRect(2,7,6,18);
  g.fillStyle="#9b4de0";g.fillRect(1,18+arm,6,11);
  g.fillStyle="#e8dcff";g.fillRect(26,18+arm,5,6);
  // Sword stays visible and swings when the attack button is pressed.
  g.save();
  if(p.atk>0){g.translate(27,21);g.rotate(-.8);g.fillStyle="#b6a2ff";g.fillRect(0,-2,25,4);g.fillStyle="#f5e8ff";g.fillRect(21,-3,6,6);g.fillStyle="#7134a8";g.fillRect(-4,-4,4,8)}
  else {g.fillStyle="#b6a2ff";g.fillRect(27,16,22,4);g.fillStyle="#f5e8ff";g.fillRect(44,13,4,3)}
  g.restore();
  if(p.atk>0){g.strokeStyle="#e8a7ff";g.lineWidth=4;g.beginPath();g.arc(30,23,30,-.8,.8);g.stroke()}
  g.restore();
}'''
html, count = re.subn(r'function drawHero\(x,y\)\{.*?\n?function drawEnemy', hero + '\nfunction drawEnemy', html, count=1, flags=re.S)
if count != 1:
    raise SystemExit("Could not safely locate drawHero() in the game HTML; no APK should be built.")

# Copy the exact same upgraded game into the HTML asset bundled in Android.
html_path.write_text(html, encoding="utf-8")
android_html = root / "android/app/src/main/assets/index.html"
android_html.parent.mkdir(parents=True, exist_ok=True)
shutil.copy2(html_path, android_html)

print("Applied 16-bit UI styling and animated pixel-style walking to Rumi.")
print(f"Updated: {html_path}")
print(f"Updated: {android_html}")
