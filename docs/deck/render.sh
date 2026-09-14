#!/bin/bash
set -e
cd "$(dirname "$0")"
CH=/opt/pw-browsers/chromium-1194/chrome-linux/chrome
mkdir -p out raw
for f in pages/s*.html; do
  n=$(basename "$f" .html)
  $CH --headless=new --no-sandbox --disable-gpu --hide-scrollbars \
      --force-device-scale-factor=1 --default-background-color=00000000 \
      --window-size=2200,1300 --screenshot="raw/$n.png" \
      --virtual-time-budget=6000 "file://$PWD/$f" 2>/dev/null
done
python3 - <<'PY'
from PIL import Image
import glob, os
for r in sorted(glob.glob('raw/s*.png')):
    im = Image.open(r).convert('RGBA')
    bb = im.getbbox()
    im = im.crop(bb) if bb else im
    im = im.convert('RGB').resize((1920,1080), Image.LANCZOS)
    out = 'out/' + os.path.basename(r)
    im.save(out)
    os.remove(r)
print('rendered', len(glob.glob('out/s*.png')))
PY
