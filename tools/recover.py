"""Recover published content from the sibling deployment repository.
Requires: python -m pip install -r tools/requirements.txt
Only run against an empty source directory; never overwrites edited posts.
"""
from pathlib import Path
from bs4 import BeautifulSoup
from markdownify import markdownify
import json
import re
import shutil
import posixpath
from urllib.parse import urlsplit, unquote

ROOT = Path(__file__).resolve().parents[1]
OLD = ROOT.parent / 'EssieYiu.github.io'
SOURCE = ROOT / 'source'
if (SOURCE / '_posts').exists():
    raise SystemExit('source/_posts already exists; refusing to overwrite recovered content')
(SOURCE / '_posts').mkdir(parents=True)
records = []

def recover_body(body, relative=""):
    # Old Jekyll Liquid remnants and duplicated relative directories caused broken images.
    for img in body.select("img"):
        src = img.get("data-original") or img.get("src", "")
        if "/assets/" in src:
            src = src[src.index("/assets/"):]
        elif src and not urlsplit(src).scheme and not src.startswith("//"):
            if not src.startswith("/"):
                if src.startswith(Path(relative).name + "/"):
                    src = str(Path(relative).parent / src)
                else:
                    src = str(Path(relative) / src)
            src = "/" + posixpath.normpath(src).lstrip("/")
        if src.endswith('.jp') and (OLD / unquote(src).lstrip('/')).with_suffix('.jpg').is_file():
            src += 'g'
        img["src"] = src
        img.attrs.pop("data-original", None)
    tokens = {}
    def protect(node, text):
        token = f'RECOVEREDTOKEN{len(tokens):06d}END'
        tokens[token] = text
        node.replace_with(token)
    for node in list(body.select('figure.highlight')):
        pre = node.select_one('td.code pre')
        if not pre:
            continue
        for br in pre.find_all('br'):
            br.replace_with('\n')
        code = pre.get_text().rstrip('\n')
        language = next((c for c in node.get('class', []) if c != 'highlight'), '')
        if language == 'plain': language = 'text'
        fence = '`' * max(3, max((len(x) + 1 for x in re.findall(r'`+', code)), default=3))
        protect(node, f'\n\n{fence}{language}\n{code}\n{fence}\n\n')
    for node in list(body.find_all('script')):
        if node.get('type', '').startswith('math/tex'):
            math = node.string or node.get_text()
            math = re.sub(r'(?<!\\)#', r'\\#', math)
            display = 'mode=display' in node.get('type', '')
            protect(node, '\n\n$$\n' + math + '\n$$\n\n' if display else '$' + math + '$')
        else:
            node.decompose()
    for node in list(body.select('a[id="more"]')):
        protect(node, '\n\n<!-- more -->\n\n')
    for img in body.find_all('img'):
        src = img.get('data-original') or img.get('src', '')
        img['src'] = src
        img.attrs = {k:v for k,v in img.attrs.items() if k in ['src','alt','title']}
    text = markdownify(str(body), heading_style='ATX', bullets='-', escape_underscores=False)
    for token, original in tokens.items():
        text = text.replace(token, original)
    return text.replace('$(#iterations)$', r'$(\#iterations)$').strip() + '\n'

for page in sorted(OLD.glob('[12][0-9][0-9][0-9]/**/index.html')):
    soup = BeautifulSoup(page.read_text(), 'html.parser')
    body = soup.select_one('.post-body')
    title = soup.select_one('.post-title').get_text(strip=True)
    date = soup.select_one('time[itemprop="dateCreated datePublished"]')['datetime']
    relative = page.parent.relative_to(OLD)
    fields = {'title': title, 'date': date, 'permalink': str(relative) + '/', 'mathjax': True,
              'disableNunjucks': True}
    categories = [n.get_text(strip=True) for n in soup.select('[itemprop="about"] [itemprop="name"]')]
    tags = [n.get_text(strip=True).lstrip('#').strip() for n in soup.select('.post-tags a')]
    if categories: fields['categories'] = categories
    if tags: fields['tags'] = tags
    header = '\n'.join(k + ': ' + json.dumps(v, ensure_ascii=False) for k,v in fields.items())
    name = '-'.join(relative.parts[:3]) + '-' + relative.name + '.md'
    (SOURCE / '_posts' / name).write_text('---\n' + header + '\n---\n\n' + recover_body(body, str(relative)))
    images = 0
    for asset in page.parent.iterdir():
        if asset.is_file() and asset.name != 'index.html':
            target = SOURCE / relative / asset.name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(asset, target)
            images += 1
    records.append({'title': title, 'source': str(page.relative_to(OLD)), 'post': name,
                    'permalink': str(relative) + '/', 'assets': images})

for folder in ['images', 'assets']:
    if (OLD / folder).exists(): shutil.copytree(OLD / folder, SOURCE / folder, dirs_exist_ok=True)
for name, title, type_ in [('about','关于',None), ('tags','标签','tags'), ('categories','分类','categories')]:
    target = SOURCE / name / 'index.md'
    target.parent.mkdir(parents=True, exist_ok=True)
    front = f'---\ntitle: {title}\n'
    if type_: front += f'type: {type_}\n'
    front += 'comments: false\n---\n\n'
    if name == 'about':
        soup = BeautifulSoup((OLD / 'about/index.html').read_text(), 'html.parser')
        front += recover_body(soup.select_one('.post-body'))
    target.write_text(front)

# Preserve historical Markdown outside source/ so it cannot be published by accident.
archive = ROOT / 'recovery' / 'original-markdown'
for p in sorted(OLD.rglob('*')):
    if p.suffix in ['.md', '.markdown'] and '.git' not in p.parts:
        target = archive / p.relative_to(OLD)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(p, target)
(ROOT / 'recovery' / 'manifest.json').write_text(json.dumps(records, ensure_ascii=False, indent=2)+'\n')
print(f'Recovered {len(records)} posts; original Markdown archived separately.')
