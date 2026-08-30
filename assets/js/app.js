document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.article h1').forEach((heading, index) => {
    if (index > 0 && heading.textContent.trim() === '산전 필라테스 지도자 교재') {
      heading.hidden = true;
    } else if (index > 0) {
      heading.classList.add('part-heading');
    }
  });

  const toc = document.querySelector('.toc-links');
  if (!toc) return;
  document.querySelectorAll('h2[id],h3[id]').forEach((heading) => {
    const link = document.createElement('a');
    link.href = '#' + heading.id;
    link.textContent = heading.textContent;
    toc.appendChild(link);
  });
});
