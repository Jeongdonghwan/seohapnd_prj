// 서하P&D — 바닐라 JS. 인트로·헤더·모바일 메뉴·스크롤 리빌·패럴랙스
(function () {
  const doc = document.documentElement;
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;

  // 인트로(스플래시): 메인 화면은 새로고침·모바일 포함 매번 1.5초
  if (!doc.classList.contains('seen')) setTimeout(() => doc.classList.add('seen'), reduce ? 0 : 1500);

  // 헤더: 스크롤 시 흰 배경
  const hd = document.getElementById('hd');
  const onScroll = () => hd.classList.toggle('solid', scrollY > 40);
  addEventListener('scroll', onScroll, { passive: true }); onScroll();

  // 모바일 메뉴
  const burger = document.getElementById('burger');
  burger.addEventListener('click', () => {
    const open = doc.classList.toggle('menu-open');
    burger.setAttribute('aria-expanded', open);
  });
  document.getElementById('gnb').addEventListener('click', e => { if (e.target.tagName === 'A') doc.classList.remove('menu-open'); });

  // 스크롤 리빌
  if (reduce || !('IntersectionObserver' in window)) {
    document.querySelectorAll('.reveal').forEach(el => el.classList.add('in'));
  } else {
    const io = new IntersectionObserver(entries => entries.forEach(en => {
      if (!en.isIntersecting) return;
      en.target.classList.add('in');
      io.unobserve(en.target);
    }), { rootMargin: '0px 0px -10% 0px', threshold: 0.1 });
    document.querySelectorAll('.reveal').forEach(el => io.observe(el));
    // 빠르게 스크롤하면 IO가 건너뛸 수 있음 → 이미 지나친 요소는 바로 노출
    let tick = 0;
    addEventListener('scroll', () => {
      if (tick) return;
      tick = setTimeout(() => {
        tick = 0;
        document.querySelectorAll('.reveal:not(.in)').forEach(el => {
          if (el.getBoundingClientRect().top < innerHeight) { el.classList.add('in'); io.unobserve(el); }
        });
      }, 150);
    }, { passive: true });
  }

  // 패럴랙스 (배경 1개)
  const par = document.querySelector('[data-parallax]');
  if (par && !reduce) {
    const move = () => {
      const r = par.parentElement.getBoundingClientRect();
      if (r.bottom < 0 || r.top > innerHeight) return;
      par.style.transform = `translateY(${(r.top + r.height / 2 - innerHeight / 2) * -0.15}px)`;
    };
    addEventListener('scroll', move, { passive: true }); move();
  }

  // 라이트박스 (인증서·공장 사진)
  const lb = document.getElementById('lightbox');
  if (lb) {
    document.querySelectorAll('.cimg[data-img]').forEach(b => b.addEventListener('click', () => {
      lb.querySelector('img').src = b.dataset.img; lb.showModal();
    }));
    lb.addEventListener('click', e => { if (e.target === lb || e.target.classList.contains('close')) lb.close(); });
  }
})();
