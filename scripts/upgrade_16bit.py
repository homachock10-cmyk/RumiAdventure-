#!/usr/bin/env python3
"""Apply a fuller 16-bit pixel-art pass to Rumi Adventure before APK/ZIP packaging."""
from pathlib import Path
import re
import shutil

root = Path("source/RumiAdventure2")
html_path = root / "index.html"
html = html_path.read_text(encoding="utf-8")

# Crisp canvas and square, pixel-era interface.
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
    '#restart{display:none;position:fixed;left:50%;top:57%;transform:translateX(-50%);border-radius:12px;',
    '#restart{display:none;position:fixed;left:50%;top:57%;transform:translateX(-50%);border-radius:0;'
)
html = html.replace(
    '#startGame{border-radius:16px;width:auto;',
    '#startGame{border-radius:0;width:auto;'
)
html = html.replace(
    'g.setTransform(D,0,0,D,0,0);floorY=',
    'g.setTransform(D,0,0,D,0,0);g.imageSmoothingEnabled=false;floorY='
)

hero = r'''function drawHero(x,y){
  const moving=Math.abs(p.vx)>1&&!over;
  const phase=t*13;
  const stride=moving?Math.round(Math.sin(phase)*5):0;
  const arm=moving?Math.round(Math.sin(phase+Math.PI)*3):0;
  const bob=moving&&p.ground?Math.abs(Math.round(Math.sin(phase)))*2:0;
  g.save();g.translate(Math.round(x),Math.round(y-bob));
  if(p.face<0){g.translate(p.w,0);g.scale(-1,1)}
  const legA=moving?stride:0,legB=moving?-stride:0;
  // Boots and legs
  g.fillStyle="#170d2b";g.fillRect(4+legA,31,9,10);g.fillRect(18+legB,31,9,10);
  g.fillStyle="#4b236f";g.fillRect(2+legA,39,12,4);g.fillRect(17+legB,39,12,4);
  // Tunic, belt and shoulder pads
  g.fillStyle="#3b195c";g.fillRect(2,11,27,24);
  g.fillStyle="#7134a8";g.fillRect(4,10,23,22);
  g.fillStyle="#9b4de0";g.fillRect(5,8,21,17);
  g.fillStyle="#f2c8ff";g.fillRect(7,12,16,10);
  g.fillStyle="#3c1a69";g.fillRect(19,13,5,4);
  g.fillStyle="#ff6bba";g.fillRect(2,7,6,18);
  g.fillStyle="#d88cff";g.fillRect(5,3,22,8);g.fillRect(8,1,15,4);
  g.fillStyle="#9b4de0";g.fillRect(1,18+arm,6,11);
  g.fillStyle="#e8dcff";g.fillRect(26,18+arm,5,6);
  g.fillStyle="#f4d7ff";g.fillRect(8,24,13,3);
  // Pixel sword, with a larger slash pose during attacks.
  g.save();
  if(p.atk>0){g.translate(27,21);g.rotate(-.8);g.fillStyle="#7134a8";g.fillRect(-4,-4,5,9);g.fillStyle="#b6a2ff";g.fillRect(0,-2,25,4);g.fillStyle="#f5e8ff";g.fillRect(20,-4,7,8)}
  else {g.fillStyle="#7134a8";g.fillRect(27,19,5,8);g.fillStyle="#b6a2ff";g.fillRect(29,16,20,4);g.fillStyle="#f5e8ff";g.fillRect(45,13,4,3)}
  g.restore();
  if(p.atk>0){g.strokeStyle="#e8a7ff";g.lineWidth=4;g.beginPath();g.arc(30,23,30,-.8,.8);g.stroke()}
  g.restore();
}'''
html, n = re.subn(r'function drawHero\(x,y\)\{.*?\n?function drawEnemy', hero + '\nfunction drawEnemy', html, count=1, flags=re.S)
if n != 1:
    raise SystemExit("Could not locate drawHero() safely.")

enemy = r'''function drawEnemy(e){
  const x=Math.round(e.x),y=Math.round(e.y),phase=t*9+e.x*.03;
  const step=e.type==="fly"?Math.round(Math.sin(phase)*3):Math.round(Math.sin(phase)*4);
  g.save();g.translate(x,y);if(e.face<0){g.translate(e.w,0);g.scale(-1,1)}
  const boss=e.type==="boss",fly=e.type==="fly";
  const body=boss?"#42104f":fly?"#392052":"#511d54";
  const light=boss?"#d12c75":fly?"#7541a4":"#a43dbe";
  // Pixel feet animate as the enemy walks.
  g.fillStyle="#21102f";g.fillRect(6+step,e.h-8,Math.max(8,e.w*.28),9);g.fillRect(e.w*.55-step,e.h-8,Math.max(8,e.w*.28),9);
  g.fillStyle=body;g.fillRect(5,9,e.w-10,e.h-12);
  g.fillStyle=light;g.fillRect(8,4,e.w-16,Math.max(8,e.h*.32));
  g.fillStyle=boss?"#ffb4f0":"#ff3d75";g.fillRect(12,14,7,5);g.fillRect(e.w-19,14,7,5);
  g.fillStyle="#fff0ff";g.fillRect(14,15,3,3);g.fillRect(e.w-17,15,3,3);
  g.fillStyle="#291035";g.fillRect(8,e.h-5,10,7);g.fillRect(e.w-18,e.h-5,10,7);
  g.fillStyle="#e4b7ff";g.fillRect(3,0,8,10);g.fillRect(e.w-11,0,8,10);
  g.fillStyle=light;g.fillRect(0,18+step,8,Math.max(12,e.h*.3));g.fillRect(e.w-8,18-step,8,Math.max(12,e.h*.3));
  if(boss){
    g.fillStyle="#9c39cb";g.fillRect(-12,18,14,34);g.fillRect(e.w-2,18,14,34);
    g.fillStyle="#ffccfa";g.fillRect(20,29,10,5);g.fillRect(e.w-30,29,10,5);
    g.fillStyle="#f5b7ff";g.fillRect(15,-8,8,12);g.fillRect(e.w-23,-8,8,12);g.fillRect(e.w/2-4,-13,8,15);
  }
  g.restore();
  if(e.hp<e.max){g.fillStyle="#351b43";g.fillRect(x,y-9,e.w,5);g.fillStyle=boss?"#ff367c":"#b968ff";g.fillRect(x,y-9,e.w*Math.max(0,e.hp/e.max),5)}
}'''
html, n = re.subn(r'function drawEnemy\(e\)\{.*?\n?function bg\(\)', enemy + '\nfunction bg()', html, count=1, flags=re.S)
if n != 1:
    raise SystemExit("Could not locate drawEnemy() safely.")

background = r'''function bg(){
  const sky=level===2?"#35132c":level===3?"#10091f":level===1?"#171033":"#101b36";
  const mid=level===2?"#7d3040":level===3?"#321545":level===1?"#33204e":"#28264e";
  const ground=level===2?"#602b3b":level===3?"#2b153b":"#2b1940";
  g.fillStyle=sky;g.fillRect(0,0,W,H);
  // Pixel stars and a blocky moon, fixed to a virtual pixel grid.
  for(let i=0;i<56;i++){g.fillStyle=i%5===0?"#e8caff":"#fff";g.globalAlpha=.45+(i%3)*.18;g.fillRect(Math.round((i*173-camera*.12)%(W+12)),Math.round(i*67%Math.max(1,H*.62)),3,3)}
  g.globalAlpha=1;
  g.fillStyle="#f1d6ff";g.fillRect(Math.round(W*.77),Math.round(H*.15),30,30);
  g.fillStyle=sky;g.fillRect(Math.round(W*.77)+7,Math.round(H*.15)-4,27,27);
  // Layered, stepped mountains scroll at different speeds.
  for(let layer=0;layer<2;layer++){
    const parallax=layer===0?.16:.28;
    const base=H*.68+layer*36;
    g.fillStyle=layer===0?mid:ground;
    for(let i=-2;i<Math.ceil(W/100)+3;i++){
      const xx=Math.round(i*100-(camera*parallax)%100);
      const peak=base-75-((i+20)%3)*22;
      g.fillRect(xx,peak,64,base-peak);
      g.fillRect(xx+16,peak-16,48,16);
      g.fillRect(xx+32,peak-28,24,12);
    }
    if(level!==0){
      g.fillStyle=layer===0?"#49305c":"#3d2353";
      for(let i=-1;i<Math.ceil(W/170)+2;i++){
        const xx=Math.round(i*170-(camera*parallax)%170+45);
        g.fillRect(xx,base-95,14,95);g.fillRect(xx-8,base-103,30,10);
      }
    }
  }
  // Low-resolution tiled ground silhouette.
  g.fillStyle=ground;g.fillRect(0,floorY,W,H-floorY);
  g.fillStyle=level===2?"#ff8c57":"#bd7aff";
  for(let x=0;x<W;x+=16){g.fillRect(x,floorY,12,4)}
}'''
html, n = re.subn(r'function bg\(\)\{.*?\nfunction draw\(\)', background + '\nfunction draw()', html, count=1, flags=re.S)
if n != 1:
    raise SystemExit("Could not locate bg() safely.")

# Make the game's drawn geometry snap to integer coordinates.
html = html.replace(
    'g.fillStyle=level===2?"#ff8c57":"#bd7aff";g.fillRect(pl.x,pl.y,pl.w,5);',
    'g.fillStyle=level===2?"#ff8c57":"#bd7aff";g.fillRect(Math.round(pl.x),Math.round(pl.y),Math.round(pl.w),5);'
)

html_path.write_text(html, encoding="utf-8")
android_html = root / "android/app/src/main/assets/index.html"
android_html.parent.mkdir(parents=True, exist_ok=True)
shutil.copy2(html_path, android_html)

# Keep an explicit build note inside the source archive.
(root / "PIXEL_ART_BUILD.txt").write_text(
    "Rumi Adventure — 16-bit style build\n"
    "The build workflow applies scripts/upgrade_16bit.py before packaging.\n"
    "Includes pixel-style UI, animated walking legs, sword swing, animated demons, and a tiled pixel-style background.\n",
    encoding="utf-8"
)
print("Applied full first-pass 16-bit pixel styling.")
print("Updated game HTML and Android bundled HTML; APK and ZIP can now be packaged.")
