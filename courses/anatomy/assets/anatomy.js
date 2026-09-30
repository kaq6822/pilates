const search = document.querySelector('#muscle-search');
if (search) search.addEventListener('input', () => {
  const query = search.value.trim().toLocaleLowerCase();
  let visible = 0;
  document.querySelectorAll('#muscle-list .muscle').forEach(link => {
    const match = link.dataset.name.toLocaleLowerCase().includes(query);
    link.hidden = !match;
    if (match) visible++;
  });
  document.querySelector('#search-empty').hidden = visible > 0;
});
document.querySelectorAll('.quiz-item[data-answer]').forEach(item => {
  item.addEventListener('change', event => {
    if (!event.target.matches('input[type="radio"]')) return;
    const correct = event.target.value === item.dataset.answer;
    item.querySelectorAll('.opt-radio').forEach(label => {
      const value = label.querySelector('input').value;
      label.classList.toggle('correct', value === item.dataset.answer);
      label.classList.toggle('wrong', value === event.target.value && !correct);
    });
    const feedback = item.querySelector('.quiz-feedback');
    feedback.textContent = correct ? '정답입니다.' : '오답입니다. 초록색 보기가 정답입니다.';
    feedback.dataset.correct = String(correct);
    const reveal = item.querySelector('.answer-reveal');
    if (reveal) reveal.open = true;
  });
});

const muscleBrowser = document.querySelector('.muscle-browser');
if (muscleBrowser) muscleBrowser.open = window.matchMedia('(min-width:761px)').matches;
const catalogSearch = document.querySelector('#catalog-search');
if (catalogSearch) catalogSearch.addEventListener('input', () => {
  const query = catalogSearch.value.trim().toLocaleLowerCase();
  let count = 0;
  document.querySelectorAll('.catalog-card').forEach(card => {
    card.hidden = !card.dataset.name.toLocaleLowerCase().includes(query);
    if (!card.hidden) count++;
  });
  document.querySelectorAll('.catalog-group').forEach(group => {
    group.hidden = !group.querySelector('.catalog-card:not([hidden])');
  });
  document.querySelector('#catalog-count').textContent = query ? `검색 결과 ${count}강` : '전체 97강';
  document.querySelector('#catalog-empty').hidden = count > 0;
});
if (search) search.addEventListener('input', () => {
  document.querySelectorAll('.muscle-group').forEach(group => {
    group.hidden = !group.querySelector('.muscle:not([hidden])');
  });
});
