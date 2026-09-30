#!/usr/bin/env python3
"""Render the two additional lessons from source Markdown and reviewed UI data."""
from pathlib import Path
import html
import json
import re

ROOT = Path(__file__).resolve().parents[1]
DATA = json.loads((ROOT / 'content/lesson_overrides.json').read_text())
CATALOG = [('M002', 'serratus-anterior', '앞톱니근', '전거근', 'Serratus anterior', '어깨·견갑대·상지')]
CATALOG += [(k, d['slug'], d['name'], d['alias'], d['en'], d['group']) for k,d in DATA.items()]
esc = html.escape

def inline(text):
    text = esc(text)
    text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'`([^`]+)`', r'<span>\1</span>', text)
    text = re.sub(r'\[([^\]]+)\]\((https?://[^)]+)\)', r'<a href="\2" target="_blank" rel="noopener">\1</a>', text)
    return text

def md(text):
    out=[]; items=[]
    def flush():
        if items:
            out.append('<ul>'+''.join('<li>'+inline(i)+'</li>' for i in items)+'</ul>');items.clear()
    for line in text.strip().splitlines():
        line=line.strip()
        if not line: flush();continue
        if line.startswith('- '):items.append(line[2:]);continue
        flush()
        if line.startswith('### '):out.append('<h3>'+inline(line[4:])+'</h3>')
        elif line.startswith('> '):out.append('<p class="note">'+inline(line[2:])+'</p>')
        else:out.append('<p>'+inline(line)+'</p>')
    flush();return '\n'.join(out)

def nav(current):
    links=''
    for key,slug,name,alias,en,group in CATALOG:
        active=' active' if key==current else ''
        aria=' aria-current="page"' if key==current else ''
        links+=f'<a class="muscle{active}" href="{key}-{slug}.html" data-name="{name} {alias} {en}"{aria}><span>{name} ({alias})<small>{group}</small></span></a>'
    return f'''<aside class="sidebar"><div class="logo"><div class="logo-mark">✦</div><div>필라테스 해부학<small>움직임을 더 깊이, 바른 지식으로</small></div></div>
<nav class="side-nav" aria-label="과정 탐색"><a href="../../index.html">⌂ 전체 학습과정</a><a href="index.html">▣ 해부학 과정</a></nav>
<label class="side-title" for="muscle-search">근육 찾기</label><input id="muscle-search" class="search" type="search" placeholder="새용어·별칭·영문명" aria-label="근육 검색"><nav id="muscle-list" aria-label="근육 학습">{links}</nav><p id="search-empty" hidden>일치하는 근육이 없습니다.</p></aside>'''

def image(name,alt,eager=False):
    return f'<img src="assets/images/{esc(name)}.jpg" alt="{esc(alt)}" width="1200" height="800"'+(' fetchpriority="high"' if eager else ' loading="lazy"')+'>'

def card(title,body):return f'<article class="big-card"><h2>{title}</h2>{body}</article>'
def movements(d,compact=False):
    cards=[]
    for title,en,img,desc,key in d['movements']:
        cards.append(f'<article class="apply-card">{image(img,title+"을 설명하는 뼈·근육 개념도")}<div class="pad"><h3>{title}</h3><small class="muted">{en}</small><p>{desc}</p><p class="motion-key">{key}</p></div></article>')
    return '<div class="apply-grid lesson-movements">'+''.join(cards)+'</div>'

def exercises(d):
    return '<div class="apply-grid">'+''.join(f'<article class="apply-card"><div class="exercise-tag">{t}</div><div class="pad"><h3>{en}</h3><p><b>목적</b> · {purpose}</p><p><b>수정</b> · {mod}</p><div class="cue">지도 문장 · “{cue}”</div></div></article>' for t,en,purpose,mod,cue in d['exercises'])+'</div>'

def quizzes(d):
    out=[]
    for i,(q,options,answer,explanation,term) in enumerate(d['quiz'],1):
        opts=''.join(f'<label class="opt-radio"><input type="radio" name="q{i}" value="{j}"><span>{esc(opt)}</span></label>' for j,opt in enumerate(options))
        note=f'<div class="termnote"><b>용어 설명:</b> {esc(term)}</div>' if term else ''
        out.append(f'<div class="quiz-item" data-answer="{answer}"><fieldset><legend>{i}. {esc(q)}</legend>{note}<div class="opts">{opts}</div><p class="quiz-feedback" aria-live="polite"></p><details class="answer-reveal"><summary>정답·해설 보기</summary><div class="answer-body"><b>정답: {esc(options[answer])}</b><p>{esc(explanation)}</p></div></details></fieldset></div>')
    return '<div class="quiz-list">'+''.join(out)+'</div>'

for key,d in DATA.items():
    source=(ROOT/f'content/{key}_{d["slug"]}.md').read_text()
    # Explicit editorial wording for terms that need Korean explanations.
    source=source.replace('Trendelenburg sign','비지지측 골반 하강 소견(Trendelenburg sign)').replace('무릎 valgus','무릎의 안쪽 이동(valgus)').replace('stance,','지지 조건(stance),').replace('한발 volume','한발 지지의 수행량').replace('ROM,','가동범위(ROM),')
    source=source.replace('DRA/coning', '복직근 이개(DRA)·배 중앙선 솟음(coning)').replace('linea alba와 DRA', '백색선(linea alba)과 복직근 이개(DRA)').replace('Rib flare', '갈비뼈 들림(rib flare)').replace('coning·통증', '배 중앙선 솟음(coning)·통증').replace('작은 chest lift', '작은 상체 들기(chest lift)').replace('ROM을', '가동범위(ROM)을')
    sections={int(n):body for n,body in re.findall(r'^## (\d+)\.[^\n]*\n(.*?)(?=^## \d+\.|\Z)',source,re.M|re.S)}
    memory=re.search(r'\*\*한 줄 기억:\*\* (.*)',source).group(1)
    related=re.findall(r'^- (.+)$',sections[9],re.M)
    facts=''.join(f'<tr><th scope="row">{label}</th><td>{esc(d[field])}</td></tr>' for label,field in [('기시','origin'),('정지','insertion'),('신경지배','nerve'),('주요 작용','action')])
    intro=f'<div class="summary-banner"><div class="memory-card"><div class="eyebrow">한 줄 기억</div><strong>{inline(memory)}</strong></div><div class="principle-card"><b>관찰에서 운동 선택까지</b><br>기시·정지·신경지배는 해부학 사실, 필라테스 적용은 교육적 해석입니다. 자세나 통증의 원인을 특정 근육 하나로 단정하지 않습니다.</div></div>'
    hero=f'<figure class="lesson-hero">{image(d["image"],d["name"]+"의 위치와 부착 관계",True)}<figcaption>{d["hero_note"]}</figcaption></figure>'
    overview=intro+'<div class="dashboard">'+hero+'<div class="right-col">'+card('기본 정보','<table class="info-table">'+facts+'</table>')+card('어디에 있는 근육인가',md(sections[1]))+'</div></div>'
    overview+='<div class="subsection"><h2>⚙ 주요 움직임과 기능</h2>'+movements(d)+'</div>'
    overview+='<div class="subsection"><h2>필라테스 적용 예시</h2>'+exercises(d)+'</div>'
    caution=sections[8].split('### 주의사항',1)[1].split('> **근거 구분',1)[0]
    overview+='<div class="subsection">'+card('관찰과 주의사항',md(caution))+'</div>'
    anatomy='<div class="detail-layout">'+card('위치와 부착점',md(sections[1]+sections[2]))+card('신경지배와 층별 관계',md(sections[3])+f'<h3>깊이와 인접 구조</h3><p>{d["depth"]}</p><h3>자료 차이와 과제 의존성</h3><p>{d["variation"]}</p>')+'</div>'
    anatomy+='<div class="subsection">'+card('촉진 및 위치 확인',md(sections[6]))+'</div>'
    anatomy+='<div class="subsection">'+card('함께 보면 좋은 근육','<div class="related-links">'+''.join('<span>'+esc(x)+'</span>' for x in related)+'</div>')+'</div>'
    anatomy+='<div class="note subsection">기시·정지는 부착 위치를 구분하는 용어입니다. 실제 움직임에서 기시가 항상 고정되고 정지만 움직이는 뜻은 아닙니다.</div>'
    movement=movements(d)+'<div class="detail-layout subsection">'+card('대표 작용과 일상 움직임',md(sections[4])+md(sections[5]))+card('움직이는 조건과 관찰',f'<p>{d["chain"]}</p><ul>'+''.join('<li>'+x+'</li>' for x in d['observe'])+'</ul>')+'</div>'
    movement+='<div class="subsection">'+card('기능적 해석 — 단정하지 말아야 할 점',md(sections[7]))+'</div>'
    movement+='<div class="subsection">'+card('용어 이해','<div class="term-grid">'+''.join(f'<div class="term-card"><b>{a}</b><p>{b}</p></div>' for a,b in d['glossary'])+'</div>')+'</div>'
    pilates=card('필라테스 적용',md(sections[8]))+'<div class="subsection"><h2>동작별 목적과 수정</h2>'+exercises(d)+'</div>'
    pilates+='<div class="termnote subsection"><b>가동범위와 레버 길이</b><br>가동범위는 실제 움직인 범위이며, 레버 길이는 회전축과 부하 사이의 역학적 거리와 관련됩니다. 범위를 줄이는 것과 레버를 짧게 하는 것은 다른 수정입니다.</div>'
    quiz='<div class="quiz-instructions"><div><h2>퀴즈 · 10문항</h2><p>답을 선택하고 정답·해설을 확인하세요. 선택과 결과는 저장되지 않습니다.</p></div><span class="score">즉시 학습 확인</span></div>'+quizzes(d)
    panes={'overview':overview,'anatomy':anatomy,'movement':movement,'pilates':pilates,'quiz':quiz}
    labels=['주요 이해','해부학 상세','움직임과 기능','필라테스 적용','퀴즈 (10문항)']
    radios=''.join(f'<input class="tab-radio" type="radio" name="section-tab" id="tab-{x}" aria-label="{label}"'+(' checked' if x=='overview' else '')+'>' for x,label in zip(panes,labels))
    tabs=''.join(f'<label class="tab" for="tab-{x}">{label}</label>' for x,label in zip(panes,labels))
    body=''.join(f'<section class="pane" id="{x}" aria-label="{label}">{panes[x]}</section>' for x,label in zip(panes,labels))
    full=f'''<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{d['name']} ({d['alias']}) · 필라테스 해부학</title><meta name="description" content="{d['name']}의 해부학, 움직임, 필라테스 적용과 10문항 퀴즈"><link rel="stylesheet" href="assets/anatomy.css"><script defer src="assets/anatomy.js"></script></head><body><div class="app">{nav(key)}<div class="content">{radios}<header class="top"><div class="title-row"><h1>{d['name']} <span>({d['alias']}) · {d['en']}</span></h1><div class="badge">예시 학습 · 콘텐츠 검토용</div></div><nav class="tabs" aria-label="학습 섹션">{tabs}</nav></header><main class="page"><div class="review-note">이미지는 움직임을 쉽게 설명하기 위해 제작한 개념도이며 전문 해부학 감수 전입니다. 세부 부착 범위와 기능은 본문을 함께 확인하세요.</div>{body}<section class="source-footer"><b>근거 자료</b>{md(sections[12].split("###",1)[0])}<p>이 콘텐츠는 필라테스 지도자 교육을 위한 자료이며 개인의 통증이나 질환을 진단·치료하기 위한 의료 조언을 대체하지 않습니다.</p></section><nav class="lesson-footer" aria-label="다른 학습 섹션"><a href="index.html">← 과정 목록</a>{''.join(f'<a href="{k}-{slug}.html">{name} →</a>' for k,slug,name,alias,en,group in CATALOG if k!=key)}</nav></main></div></div></body></html>'''
    (ROOT/f'{key}-{d["slug"]}.html').write_text(full)

# Existing lesson keeps its hand-edited learning content; only navigation is shared.
p=ROOT/'M002-serratus-anterior.html';s=(ROOT/'templates/serratus.html').read_text()
s=re.sub(r'<aside class="sidebar">.*?</aside>',nav('M002'),s,count=1,flags=re.S)
if 'assets/anatomy.js' not in s:s=s.replace('</head>','<script defer src="assets/anatomy.js"></script></head>')
p.write_text(s)
print('Built M001 and M003; updated navigation in M002.')

from full_course import build_course
build_course(ROOT, md, inline, card)
