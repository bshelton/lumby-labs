"""Check generated local links, fragments, assets, and page landmarks."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import sys
root = Path(__file__).resolve().parent/'_site'
class Page(HTMLParser):
    def __init__(self,text):
        super().__init__();self.links=[];self.ids=set();self.h1=0;self.main=0;self.lang=False;self.feed(text)
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if 'id' in a:self.ids.add(a['id'])
        if tag=='h1':self.h1+=1
        if tag=='main':self.main+=1
        if tag=='html':self.lang=a.get('lang')=='en'
        if tag in ('a','link') and a.get('href'):self.links.append(a['href'])
        if tag=='img':
            assert 'alt' in a,'Image missing alt text'
            self.links.append(a['src'])
pages={p.resolve():Page(p.read_text()) for p in root.rglob('*.html')}
errors=[]
for p,page in pages.items():
    if page.h1!=1 or page.main!=1 or not page.lang:errors.append(f'{p.name}: missing/duplicate landmark')
    for href in page.links:
        u=urlsplit(href)
        if u.scheme or u.netloc:continue
        target=unquote(u.path)
        if target.startswith('/lumby-labs/'):dest=root/target.removeprefix('/lumby-labs/')
        else:dest=p.parent/target if target else p
        if dest.is_dir():dest=dest/'index.html'
        dest=dest.resolve()
        if not dest.exists():errors.append(f'{p.relative_to(root)}: broken link {href}')
        elif u.fragment and dest in pages and unquote(u.fragment) not in pages[dest].ids:errors.append(f'{p.name}: missing fragment {href}')
if errors:sys.exit('\n'.join(errors))
print(f'Checked {len(pages)} pages: internal links, fragments, assets, and landmarks pass.')
