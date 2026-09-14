import re, os
html = open('_part1.html', encoding='utf-8').read() + "\n" + open('_part2.html', encoding='utf-8').read()
parts = re.findall(r'<div class="slide.*?(?=<div class="slide|\Z)', html, re.S)
total = len(parts)
os.makedirs('pages', exist_ok=True)
head = ('<!doctype html><meta charset="utf-8">'
        '<link rel="stylesheet" href="../fonts.css"><link rel="stylesheet" href="../deck.css">')
for i, p in enumerate(parts, 1):
    p = p.replace('src="img/', 'src="../img/')
    p = re.sub(r'<div class="pg">\s*\d+\s*/\s*\d+\s*</div>',
               f'<div class="pg">{i:02d} / {total}</div>', p)
    open(f'pages/s{i:02d}.html', 'w', encoding='utf-8').write(head + p)
print('slides written:', total)
