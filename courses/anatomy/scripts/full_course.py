"""Compile the complete source collection; keep editorial examples intact."""
import re
import html
from collections import defaultdict

E = html.escape
TABS = [('overview','주요 이해'),('anatomy','해부학 상세'),('movement','움직임과 기능'),('pilates','필라테스 적용'),('quiz','퀴즈 (10문항)')]

def build_course(root, md, inline, card):
    lessons=[]
    master=(root/'content/MASTER_INDEX.md').read_text()
    curriculum={}
    group_order=[]
    for group,body in re.findall(r'^### Part \d+ — ([^\n]+)\n(.*?)(?=^### Part |\Z)',master,re.M|re.S):
        group_order.append(group)
        for filename in re.findall(r'`(M\d{3}_[^`]+\.md)`',body):
            curriculum.setdefault(filename,group)
    for path in sorted((root/'content').glob('M[0-9][0-9][0-9]_*.md')):
        text=path.read_text()
        meta=dict(re.findall(r'^(\w+): (.+)$',text.split('---')[1],re.M))
        sections={int(n):body.strip() for n,body in re.findall(r'^## (\d+)\.[^\n]*\n(.*?)(?=^## \d+\.|\Z)',text,re.M|re.S)}
        assert set(range(1,13)) <= sections.keys(), path
        meta['part']=curriculum.get(path.name,meta['part'])
        meta.update(sections=sections, text=text, file=f'{meta["id"]}-{meta["slug"]}.html')
        lessons.append(meta)
    groups={group:[] for group in group_order}
    for d in lessons: groups[d['part']].append(d)
    def title(d): return f'{d["name_ko"]} ({d["name_ko_alias"]})'
    def link(d, current=''):
        return f'<a class="muscle{" active" if d["id"]==current else ""}" href="{d["file"]}" data-name="{E(title(d)+" "+d["name_en"]+" "+d["part"])}"'+(' aria-current="page"' if d['id']==current else '')+f'><span>{E(title(d))}<small>{E(d["name_en"])}</small></span></a>'
    def nav(current):
        items=''.join(f'<section class="muscle-group"><h2>{E(group)}</h2>'+''.join(link(d,current) for d in entries)+'</section>' for group,entries in groups.items())
        return f'<aside class="sidebar"><div class="logo">필라테스 해부학</div><nav class="side-nav" aria-label="과정 탐색"><a href="../../index.html">전체 학습과정</a><a href="index.html">해부학 전체 97강</a></nav><details class="muscle-browser" open><summary>근육 탐색 · 97강</summary><label class="side-title" for="muscle-search">이름 또는 부위로 검색</label><input id="muscle-search" class="search" type="search" placeholder="새용어·별칭·영문명·부위"><nav id="muscle-list" aria-label="근육 학습">{items}</nav><p id="search-empty" hidden>일치하는 근육이 없습니다.</p></details></aside>'
    def placeholder(label): return f'<div class="image-placeholder" role="img" aria-label="{E(label)} — 이미지 준비 전"><span>이미지 준비 중</span></div>'
    def related(s):
        out=[]
        for name in re.findall(r'^- (.+)$',s,re.M):
            matches=[d for d in lessons if name in (d['name_ko'],d['name_ko_alias'])]
            out.append(f'<a href="{matches[0]["file"]}">{E(name)}</a>' if matches else f'<span>{E(name)}</span>')
        return '<div class="related-links">'+''.join(out)+'</div>'
    def quiz(s):
        questions,answers=s.split('<details>',1)
        qs=re.findall(r'^(\d+)\. (.+)$',questions,re.M)
        ans=dict(re.findall(r'^(\d+)\. (.+)$',answers,re.M))
        assert len(qs)==10 and len(ans)==10
        out='<div class="quiz-instructions"><div><h2>퀴즈 · 10문항</h2><p>답을 떠올리거나 작성한 뒤 모범 답안과 비교하세요. 작성 내용은 저장되지 않습니다.</p></div><span class="score">학습 확인</span></div>'
        for n,q in qs:
            q=q.replace('[위치 선택 · 기본]','[부착점 회상 · 기본]').replace('그림에서 ', '').replace('을 선택하시오.','을 설명하시오.')
            a=ans[n].replace('Section 4와 Section 7','움직임과 기능 탭의 주요 작용과 기능적 해석')
            out+=f'<article class="quiz-item"><h3 id="question-{n}">{n}. {inline(q)}</h3><textarea rows="3" aria-labelledby="question-{n}" placeholder="나의 답을 적어 보세요"></textarea><details class="answer-reveal"><summary>정답·해설 보기</summary><div class="answer-body">{inline(a)}</div></details></article>'
        return out
    for i,d in enumerate(lessons):
        p=root/d['file'];s=d['sections']
        if d['id'] not in ('M001','M002','M003'):
            memory=re.search(r'\*\*한 줄 기억:\*\* (.+)',d['text']).group(1)
            overview=f'<div class="memory-card"><div class="eyebrow">한 줄 기억</div><strong>{inline(memory)}</strong></div><div class="dashboard subsection"><figure class="lesson-hero">{placeholder(d["name_ko"]+" 위치도")}<figcaption>{E(title(d))} · {E(d["name_en"])}</figcaption></figure><div class="right-col">'+card('어디에 있는 근육인가',md(s[1]))+card('주요 작용',md(s[4]))+'</div></div><div class="detail-layout subsection">'+card('기시 · 정지',md(s[2]))+card('신경지배',md(s[3]))+'</div><div class="subsection">'+card('일상 움직임',md(s[5]))+'</div>'
            anatomy='<div class="detail-layout">'+card('위치와 부착점',md(s[1]+ '\n\n'+s[2]))+card('신경지배와 위치 확인',md(s[3])+ '<h3>촉진 및 위치 확인</h3>'+md(s[6]))+'</div><div class="subsection">'+card('함께 보면 좋은 근육',related(s[9]))+'</div>'
            movement='<div class="detail-layout">'+card('주요 작용',md(s[4]))+card('일상 움직임',md(s[5]))+'</div><div class="subsection">'+card('기능적 해석 — 단정하지 말아야 할 점',md(s[7]))+'</div>'
            panes=[overview,anatomy,movement,card('필라테스 적용',md(s[8])),quiz(s[11])]
            radios=''.join(f'<input class="tab-radio" type="radio" name="section-tab" id="tab-{key}" aria-label="{label}"'+(' checked' if key=='overview' else '')+'>' for key,label in TABS)
            tabs=''.join(f'<label class="tab" for="tab-{key}">{label}</label>' for key,label in TABS)
            body=''.join(f'<section class="pane" id="{key}" aria-label="{label}">{body}</section>' for (key,label),body in zip(TABS,panes))
            page=f'<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{E(title(d))} · 필라테스 해부학</title><link rel="stylesheet" href="assets/anatomy.css"><script defer src="assets/anatomy.js"></script></head><body><div class="app">{nav(d["id"])}<div class="content">{radios}<header class="top"><div class="title-row"><h1>{E(d["name_ko"])} <span>({E(d["name_ko_alias"])}) · {E(d["name_en"])}</span></h1><div class="badge">{E(d["part"])}</div></div><nav class="tabs" aria-label="학습 섹션">{tabs}</nav></header><main class="page"><p class="review-note">해부학적 사실과 필라테스 적용을 구분해 학습하세요. 자세나 통증의 원인을 근육 하나로 단정하지 않습니다.</p>{body}<section class="source-footer"><h2>근거 자료</h2>{md(s[12].split("###",1)[0])}</section></main></div></div></body></html>'
        else:
            page=p.read_text()
            page=re.sub(r'<aside class="sidebar">.*?</aside>',lambda _:nav(d['id']),page,count=1,flags=re.S)
            page=re.sub(r'<img\b[^>]*>',lambda m:placeholder((re.search(r'alt="([^"]*)"',m[0]) or ['','해부학 이미지'])[1]),page)
            page=re.sub(r'<p class="motion-key">.*?</p>','',page,flags=re.S)
            page=re.sub(r'<div class="review-note">.*?</div>','<div class="review-note">이미지는 준비 중입니다. 위치와 움직임은 본문 설명을 통해 학습하세요.</div>',page,flags=re.S)
            page=page.replace('예시 학습 · 콘텐츠 검토용','해부학 학습')
        page=re.sub(r'<nav class="lesson-footer".*?</nav>','',page,flags=re.S)
        footer='<nav class="lesson-footer" aria-label="학습 이동"><a href="index.html">전체 97강 목록</a>'
        if i: footer+=f'<a href="{lessons[i-1]["file"]}">← {E(lessons[i-1]["name_ko"])}</a>'
        if i+1<len(lessons): footer+=f'<a href="{lessons[i+1]["file"]}">{E(lessons[i+1]["name_ko"])} →</a>'
        page=page.replace('</main>',footer+'</nav></main>')
        p.write_text(page)
    sections=''
    for i,(group,entries) in enumerate(groups.items(),1):
        cards=''.join(f'<a class="catalog-card" href="{d["file"]}" data-name="{E(title(d)+" "+d["name_en"]+" "+group)}"><small>{d["id"]} · 5개 탭 · 10문항</small><h3>{E(title(d))}</h3><p>{E(d["name_en"])}</p><span>학습 시작 →</span></a>' for d in entries)
        sections+=f'<section class="catalog-group" id="part-{i}"><h2>{E(group)} <small>{len(entries)}강</small></h2><div class="catalog-grid">{cards}</div></section>'
    jumps=''.join(f'<a href="#part-{i}">{E(group)}</a>' for i,group in enumerate(groups,1))
    (root/'index.html').write_text(f'<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>필라테스 해부학 · 전체 과정</title><link rel="stylesheet" href="assets/anatomy.css"><script defer src="assets/anatomy.js"></script></head><body><main class="catalog"><a class="back-link" href="../../index.html">← 전체 학습과정</a><header class="catalog-hero"><span>PILATES ANATOMY</span><h1>움직임을 이해하는<br>필라테스 해부학</h1><p>위치와 부착점부터 움직임, 필라테스 적용까지.<br>97개 근육 학습과 970개 확인 문제로 연결합니다.</p></header><section class="catalog-tools"><label for="catalog-search">배우고 싶은 근육을 찾아보세요</label><input id="catalog-search" type="search" placeholder="새용어, 구용어, 영문명 또는 부위 검색"><p id="catalog-count" role="status">전체 97강</p><nav class="part-links" aria-label="부위별 바로가기">{jumps}</nav></section><p id="catalog-empty" hidden>검색 결과가 없습니다. 다른 이름이나 부위를 입력해 보세요.</p>{sections}</main></body></html>')
    print(f'Built complete course: {len(lessons)} lessons, {len(lessons)*10} questions.')
