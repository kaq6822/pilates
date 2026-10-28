#!/usr/bin/env python3
"""Build a text-only, quiz-free EPUB 3 from the current anatomy lesson pages."""
import argparse
import html
from html.parser import HTMLParser
from pathlib import Path
import re
import uuid
import zipfile
from datetime import datetime, timezone
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
XHTML = 'http://www.w3.org/1999/xhtml'
ET.register_namespace('', XHTML)
TABS = [('overview', '주요 이해'), ('anatomy', '해부학 상세'), ('movement', '움직임과 기능'), ('pilates', '필라테스 적용')]
VOID = {'area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr'}
SKIP = {'script','style','img','input','button'}
ALLOWED = {'section','article','div','p','span','h1','h2','h3','h4','h5','h6','ul','ol','li','strong','b','em','i','small','br','hr','table','thead','tbody','tfoot','tr','th','td','a','blockquote','figure','figcaption','dl','dt','dd','sup','sub'}

class Node:
    def __init__(self, tag, attrs=()): self.tag, self.attrs, self.children = tag, dict(attrs), []

class Parser(HTMLParser):
    def __init__(self): super().__init__(convert_charrefs=True); self.root=Node('root'); self.stack=[self.root]
    def handle_starttag(self, tag, attrs):
        n=Node(tag,attrs); self.stack[-1].children.append(n)
        if tag not in VOID: self.stack.append(n)
    def handle_startendtag(self, tag, attrs): self.handle_starttag(tag,attrs); self.handle_endtag(tag) if tag not in VOID else None
    def handle_endtag(self, tag):
        for i in range(len(self.stack)-1,0,-1):
            if self.stack[i].tag==tag: del self.stack[i:]; break
    def handle_data(self, text): self.stack[-1].children.append(text)

def find(n, pred):
    if pred(n): return n
    for c in n.children:
        if isinstance(c,Node):
            result=find(c,pred)
            if result: return result
    return None

def content(n): return ''.join(c if isinstance(c,str) else content(c) for c in n.children)

def render(n, known):
    if isinstance(n,str): return html.escape(n)
    cls=n.attrs.get('class','').split()
    if n.tag in SKIP or 'image-placeholder' in cls or 'motion-key' in cls: return ''
    inner=''.join(render(c,known) for c in n.children)
    if n.tag not in ALLOWED: return inner
    attrs=''
    if n.tag=='a':
        href=n.attrs.get('href','')
        if href.startswith(('https://','http://','mailto:')): attrs=' href="'+html.escape(href,quote=True)+'"'
        elif href.split('#')[0] in known:
            dest,_,frag=href.partition('#'); attrs=' href="'+html.escape(known[dest]+('#'+frag if frag else ''),quote=True)+'"'
        else: return inner
    if n.tag in ('th','td'):
        for key in ('colspan','rowspan','scope'):
            if key in n.attrs: attrs+=' '+key+'="'+html.escape(n.attrs[key],quote=True)+'"'
    if n.tag in ('br','hr'): return '<'+n.tag+' />'
    return '<'+n.tag+attrs+'>'+inner+'</'+n.tag+'>'

def document(title, body):
    return ('<?xml version="1.0" encoding="utf-8"?>\n<!DOCTYPE html>\n'
        '<html xmlns="'+XHTML+'" lang="ko" xml:lang="ko"><head><title>'+html.escape(title)+'</title>'
        '<link rel="stylesheet" type="text/css" href="style.css" /></head><body>'+body+'</body></html>')

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--output',type=Path,default=ROOT/'dist/pilates-anatomy.epub')
    ap.add_argument('--title',default='필라테스 해부학')
    ap.add_argument('--author',default='',help='출판용 저자명')
    ap.add_argument('--publisher',default='',help='출판사 또는 발행자')
    ap.add_argument('--identifier',default='urn:uuid:1597ee40-86bc-5b65-8e5b-6087d656a319',help='도서 식별자 (확정된 경우 ISBN 등)')
    args=ap.parse_args()
    files=sorted(ROOT.glob('M[0-9][0-9][0-9]-*.html'))
    if len(files)!=97: raise SystemExit(f'예상한 97개 강의가 아닙니다: {len(files)}개')
    known={f.name:f.stem+'.xhtml' for f in files}; lessons=[]
    for f in files:
        p=Parser(); p.feed(f.read_text(encoding='utf-8'))
        h=find(p.root,lambda n:n.tag=='h1')
        if h is None: raise ValueError(f'{f}: 제목 없음')
        title=' '.join(content(h).split()); sections=[]
        for ident,label in TABS:
            n=find(p.root,lambda n:n.tag=='section' and n.attrs.get('id')==ident)
            if n is None: raise ValueError(f'{f}: {ident} 탭 없음')
            sections.append('<section><h2>'+label+'</h2>'+''.join(render(c,known) for c in n.children)+'</section>')
        source=find(p.root,lambda n:n.tag=='section' and 'source-footer' in n.attrs.get('class','').split())
        if source is None: raise ValueError(f'{f}: 근거 자료 없음')
        body='<h1>'+html.escape(title)+'</h1>'+''.join(sections)+'<section>'+''.join(render(c,known) for c in source.children)+'</section>'
        doc=document(title,body); ET.fromstring(doc); lessons.append((known[f.name],title,doc))
    toc='<nav xmlns:epub="http://www.idpf.org/2007/ops" epub:type="toc" id="toc"><h1>목차</h1><ol>'+''.join('<li><a href="'+html.escape(name)+'">'+html.escape(title)+'</a></li>' for name,title,_ in lessons)+'</ol></nav>'
    nav=document('목차',toc); ET.fromstring(nav)
    metadata='<dc:identifier id="pub-id">'+html.escape(args.identifier)+'</dc:identifier><dc:title>'+html.escape(args.title)+'</dc:title><dc:language>ko</dc:language>'
    if args.author: metadata+='<dc:creator>'+html.escape(args.author)+'</dc:creator>'
    if args.publisher: metadata+='<dc:publisher>'+html.escape(args.publisher)+'</dc:publisher>'
    metadata+='<meta property="dcterms:modified">'+datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')+'</meta>'
    manifest='<item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav"/><item id="css" href="style.css" media-type="text/css"/>'
    manifest+=''.join(f'<item id="lesson{i}" href="{html.escape(name)}" media-type="application/xhtml+xml"/>' for i,(name,_,_) in enumerate(lessons))
    spine=''.join(f'<itemref idref="lesson{i}"/>' for i in range(len(lessons)))
    opf='<?xml version="1.0" encoding="utf-8"?><package xmlns="http://www.idpf.org/2007/opf" xmlns:dc="http://purl.org/dc/elements/1.1/" version="3.0" unique-identifier="pub-id"><metadata>'+metadata+'</metadata><manifest>'+manifest+'</manifest><spine>'+spine+'</spine></package>'
    ET.fromstring(opf)
    container='<?xml version="1.0" encoding="UTF-8"?><container xmlns="urn:oasis:names:tc:opendocument:xmlns:container" version="1.0"><rootfiles><rootfile full-path="OEBPS/package.opf" media-type="application/oebps-package+xml"/></rootfiles></container>'
    css='body { line-height: 1.6; margin: 5%; } h1 { font-size: 1.6em; } h2 { margin-top: 1.5em; } p, li { line-height: 1.6; } table { border-collapse: collapse; max-width: 100%; } th, td { border: 1px solid #888; padding: 0.3em; text-align: left; } a { color: #164b82; }'
    args.output.parent.mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(args.output,'w') as z:
        z.writestr('mimetype','application/epub+zip',compress_type=zipfile.ZIP_STORED)
        for name,data in [('META-INF/container.xml',container),('OEBPS/package.opf',opf),('OEBPS/nav.xhtml',nav),('OEBPS/style.css',css)]+[('OEBPS/'+name,doc) for name,_,doc in lessons]: z.writestr(name,data,compress_type=zipfile.ZIP_DEFLATED)
    print(f'{args.output}: {len(lessons)}강, 퀴즈와 이미지 제외')
if __name__=='__main__': main()
