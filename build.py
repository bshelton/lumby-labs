"""Build the Lumby Labs static site using Python's standard library."""
from pathlib import Path
import shutil
from html import escape

ROOT = Path(__file__).resolve().parent
OUT = ROOT / '_site'
DOCS = [('', 'Overview', 'overview'), ('getting-started/', 'Getting started', 'getting-started'), ('runs-and-settings/', 'Runs & settings', 'runs-and-settings'), ('accounting/', 'Profit & costs', 'accounting'), ('herb-sacks/', 'Herb sacks', 'herb-sacks'), ('troubleshooting/', 'Troubleshooting', 'troubleshooting')]
BASE = 'docs/farming-run-profit/'

def link(href, text, current=False):
    return f'<a href="{href}"'+(' aria-current="page"' if current else '')+f'>{escape(text)}</a>'

def shell(path, title, description, body, active='plugins'):
    prefix = '../' * len([p for p in path.split('/') if p])
    if path == '404.html': prefix = '/lumby-labs/'
    nav = ''.join([link(prefix, 'Plugins', active=='plugins'),link(prefix+BASE,'Docs',active=='docs'),link(prefix+'help/','Help',active=='help'),link('https://github.com/bshelton/lumby-labs','GitHub')])
    body = body.replace('{{root}}', prefix)
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{escape(title)} · Lumby Labs</title><meta name="description" content="{escape(description,quote=True)}"><meta name="theme-color" content="#faf9f5"><link rel="icon" href="{prefix}assets/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="{prefix}assets/site.css"></head>
<body><a class="skip" href="#main">Skip to content</a><header class="site-header"><div class="wrap header-inner"><a class="brand" href="{prefix or './'}"><span class="monogram" aria-hidden="true">LL</span>Lumby Labs</a><nav class="main-nav" aria-label="Main navigation">{nav}</nav></div></header>
<main id="main" class="wrap">{body}</main>
<footer class="site-footer"><div class="wrap footer-inner"><p><strong>Lumby Labs</strong><br>Independent plugins for RuneLite.</p><p>Not affiliated with Jagex or RuneLite.<br><a href="{prefix}help/">Help &amp; support</a> · <a href="https://github.com/bshelton/lumby-labs">Website source</a></p></div></footer></body></html>'''

def write(path, title, description, body, active='plugins'):
    dest = OUT / path if path.endswith('.html') else OUT / path / 'index.html'
    dest.parent.mkdir(parents=True,exist_ok=True)
    dest.write_text(shell(path,title,description,body,active))

def build():
    if OUT.exists(): shutil.rmtree(OUT)
    OUT.mkdir()
    shutil.copytree(ROOT/'assets', OUT/'assets')
    (OUT/'.nojekyll').touch()
    home='''<section class="hero"><h1>A little less friction.<br>A little more game.</h1><p>RuneLite plugins from Lumby Labs. Useful tools for your everyday routes, with clear guides when you need a hand.</p></section>
<section aria-labelledby="plugins-title"><div class="section-heading"><h2 id="plugins-title">The plugin collection</h2><span class="quiet">One plugin. Room to grow.</span></div>
<article class="plugin-entry"><div><div class="plugin-title"><img src="{{root}}assets/farming-run-profit.png" alt="" width="48" height="48"><div><h2>Farming Run Profit</h2><span class="status">Available in the Plugin Hub</span></div></div><p>Know what your farming run earned. Track harvests, seeds, compost, and supported travel costs in one itemized ledger, with herb-sack support and saved run history.</p><div class="actions"><a class="button" href="{{root}}docs/farming-run-profit/">Read the guide</a><a href="https://runelite.net/plugin-hub/show/farming-profit-tracker">Get the plugin</a></div></div><dl class="facts"><div><dt>Category</dt><dd>Farming</dd></div><div><dt>Run history</dt><dd>Stored locally</dd></div><div><dt>Source</dt><dd><a href="https://github.com/bshelton/farming-profit">GitHub</a></dd></div><div><dt>Support</dt><dd><a href="https://github.com/bshelton/farming-profit/issues">GitHub Issues</a></dd></div></dl></article></section>
<section class="help-strip"><div><h2>A question, a bug, or an idea?</h2><p>Find the right guide or open an issue for the plugin you use.</p></div><a href="{{root}}help/">Find help &amp; support</a></section>'''
    write('', 'RuneLite plugins & documentation', 'Discover RuneLite plugins by Lumby Labs. Read setup guides, understand features, and find help through GitHub Issues.', home)
    for i,(slug,label,source) in enumerate(DOCS):
        path=BASE+slug
        sidebar='<h2>Farming Run Profit</h2><nav aria-label="Plugin documentation">'+''.join(link('{{root}}'+BASE+s,l,s==slug) for s,l,_ in DOCS)+'</nav><div class="support-nav">'+link('{{root}}help/','Get help / report a bug')+link('https://github.com/bshelton/farming-profit','Plugin source')+'</div>'
        mobile='<details class="mobile-doc-nav"><summary>In this guide</summary><nav aria-label="Mobile documentation">'+''.join(link('{{root}}'+BASE+s,l,s==slug) for s,l,_ in DOCS)+'</nav></details>'
        content=(ROOT/'content'/f'{source}.html').read_text()
        previous = link('{{root}}'+BASE+DOCS[i-1][0], 'Previous: '+DOCS[i-1][1]) if i else link('{{root}}','All plugins')
        nextlink = link('{{root}}'+BASE+DOCS[i+1][0], 'Next: '+DOCS[i+1][1]) if i+1<len(DOCS) else link('{{root}}help/','Get help')
        body=f'<div class="docs-layout"><aside class="doc-nav">{sidebar}</aside><div>{mobile}<article class="article">{content}<nav class="doc-next" aria-label="Guide pages">{previous}{nextlink}</nav></article></div></div>'
        write(path, label+' — Farming Run Profit', f'{label} for Farming Run Profit, a RuneLite plugin by Lumby Labs.', body,'docs')
    write('help/','Help & support','Report a bug, suggest a feature, or get help with Lumby Labs RuneLite plugins.', '<article class="article simple-page">'+(ROOT/'content/help.html').read_text()+'</article>','help')
    write('404.html','Page not found','Find Lumby Labs plugin guides and support.', '<div class="not-found"><h1>This page wandered off.</h1><p>Head back to the plugin collection or find the guide you need.</p><a class="button" href="{{root}}">Back to plugins</a></div>')
    print('Built 9 static pages in _site/')

if __name__=='__main__': build()
