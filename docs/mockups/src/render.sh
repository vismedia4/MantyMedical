#!/bin/bash
set -e
cd "$(dirname "$0")"
CH=/opt/pw-browsers/chromium-1194/chrome-linux/chrome
shot () { # file W H
  $CH --headless=new --no-sandbox --disable-gpu --hide-scrollbars \
      --force-device-scale-factor=2 --default-background-color=00000000 \
      --window-size=$2,$3 --screenshot=raw-$1.png --virtual-time-budget=5000 \
      "file://$PWD/$1.html" 2>/dev/null
}
shot 01-passport-status 560 1140
shot 02-crew-queue      560 1140
shot 03-console-floor   1600 1080
python3 - <<'PY'
from PIL import Image
import glob, os
for r in sorted(glob.glob('raw-*.png')):
    im = Image.open(r).convert('RGBA')
    bb = im.getbbox()          # bounding box of non-transparent pixels
    if bb:
        pad = 24
        l,t,rr,b = bb
        l=max(0,l-pad); t=max(0,t-pad); rr=min(im.width,rr+pad); b=min(im.height,b+pad)
        im = im.crop((l,t,rr,b))
    out = r.replace('raw-','pioneer-')
    im.save(out)
    print(out, im.size)
    os.remove(r)
PY
