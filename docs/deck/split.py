import re, os
html = open('_part1.html').read() + "\n" + open('_part2.html').read()
parts = re.findall(r'<div class="slide.*?(?=<div class="slide|\Z)', html, re.S)
os.makedirs('pages', exist_ok=True)
head = ('<!doctype html><meta charset="utf-8">'
        '<link rel="stylesheet" href="../fonts.css"><link rel="stylesheet" href="../deck.css">')
for i, p in enumerate(parts, 1):
    p = p.replace('src="img/', 'src="../img/')
    open(f'pages/s{i:02d}.html', 'w').write(head + p)
print('slides written:', len(parts))
