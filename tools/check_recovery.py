"""Compare rebuilt articles with the archived deployment; run after npm run build."""
from pathlib import Path
from bs4 import BeautifulSoup
from urllib.parse import urlsplit, unquote
import json
import posixpath

ROOT = Path(__file__).resolve().parents[1]
OLD = ROOT.parent / 'EssieYiu.github.io'
records = json.loads((ROOT / 'recovery/manifest.json').read_text())
errors, missing = [], []
code_count = math_count = image_count = 0
for row in records:
    page = ROOT / 'public' / row['permalink'] / 'index.html'
    if not page.exists():
        errors.append('Missing article: ' + row['permalink'])
        continue
    old = BeautifulSoup((OLD / row['source']).read_text(), 'html.parser').select_one('.post-body')
    new = BeautifulSoup(page.read_text(), 'html.parser')
    body = new.select_one('.post-body')
    if new.select_one('.post-title').get_text(strip=True) != row['title']:
        errors.append('Title mismatch: ' + row['title'])
    def code_blocks(node):
        result=[]
        for pre in node.select('figure.highlight td.code pre'):
            for br in pre.select('br'): br.replace_with('\n')
            result.append(pre.get_text().rstrip('\n'))
        return result
    before, after = code_blocks(old), code_blocks(body)
    if before != after: errors.append('Code mismatch: ' + row['title'])
    code_count += len(before)
    equations = old.select('script[type^="math/tex"]')
    rendered = body.select('mjx-container')
    if len(rendered) < len(equations):
        errors.append(f'Math count: {row["title"]}: {len(equations)} -> {len(rendered)}')
    if body.select('[data-mjx-error], mjx-merror'):
        errors.append('Math rendering error: ' + row['title'])
    math_count += len(rendered)
    if len(old.select('img')) != len(body.select('img')):
        errors.append('Image count mismatch: ' + row['title'])
    for img in body.select('img'):
        src = img.get('src', '')
        if urlsplit(src).scheme or src.startswith('//'): continue
        image_count += 1
        path = unquote(urlsplit(src).path)
        path = path if path.startswith('/') else '/' + row['permalink'] + path
        path = posixpath.normpath(path).lstrip('/')
        if not (ROOT / 'public' / path).is_file():
            missing.append({'article':row['title'], 'image':src})
    if 'RECOVEREDTOKEN' in body.get_text(): errors.append('Unrestored recovery token')
for path in ['index.html', 'about/index.html', 'archives/index.html', 'tags/index.html', 'categories/index.html']:
    if not (ROOT / 'public' / path).is_file(): errors.append('Missing page: ' + path)
report={'posts':len(records),'code_blocks':code_count,'rendered_equations':math_count,
        'local_images':image_count,'missing_images':missing,'errors':errors}
(ROOT / 'recovery/validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(report,ensure_ascii=False,indent=2))
raise SystemExit(bool(errors or missing))
