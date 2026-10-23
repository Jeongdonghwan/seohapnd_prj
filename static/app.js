// 서하P&D — 바닐라 JS. 인트로·헤더·모바일 메뉴·스크롤 리빌·패럴랙스
(function () {
  const doc = document.documentElement;
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;

  // 인트로(스플래시): 메인 화면은 새로고침·모바일 포함 매번 1.5초
  if (!doc.classList.contains('seen')) setTimeout(() => doc.classList.add('seen'), reduce ? 0 : 1500);

  // 히어로 영상: 세로 화면이면 모바일용, 가로면 PC용. 동작 줄이기 설정이면 첫 장면 사진만
  const hv = document.getElementById('heroVideo');
  if (hv) {
    const portrait = matchMedia('(orientation: portrait)');
    const pick = () => {
      const k = portrait.matches ? 'mo' : 'pc';
      hv.poster = hv.dataset[k + 'Poster'];
      if (reduce || hv.dataset.cur === k) return;
      hv.dataset.cur = k; hv.src = hv.dataset[k];
      hv.play().catch(() => {});      // 저전력 모드 등으로 막히면 포스터가 그대로 보임
    };
    pick();
    portrait.addEventListener ? portrait.addEventListener('change', pick) : portrait.addListener(pick);

    // 소리: 브라우저는 클릭 전 소리 자동재생을 막음 → 무음 재생, 첫 클릭·터치·키 입력 때 켜짐. 버튼으로 끄면 다시 안 켬
    const btn = document.getElementById('heroSound');
    if (!reduce) {
      let userOff = false;
      try { userOff = sessionStorage.getItem('heroSound') === 'off'; } catch (e) {}
      hv.volume = 0.6;
      const setSound = on => {
        hv.muted = !on;
        if (on) hv.play().catch(() => {});
        btn.classList.toggle('on', on);
        btn.setAttribute('aria-pressed', on);
        btn.querySelector('span').textContent = on ? '소리 끄기' : '소리 켜기';
      };
      btn.hidden = false;
      btn.addEventListener('click', () => {
        const on = hv.muted;
        userOff = !on;
        try { sessionStorage.setItem('heroSound', on ? 'on' : 'off'); } catch (e) {}
        setSound(on);
      });
      const firstGesture = e => {
        ['pointerdown', 'keydown'].forEach(t => removeEventListener(t, firstGesture, true));
        if (!userOff && !btn.contains(e.target)) setSound(true);
      };
      ['pointerdown', 'keydown'].forEach(t => addEventListener(t, firstGesture, true));

      // 히어로가 화면 밖이면 멈춤 (아래 읽는 동안 음악·배터리 낭비 방지)
      new IntersectionObserver(([en]) => {
        if (en.isIntersecting) hv.play().catch(() => {}); else hv.pause();
      }, { threshold: 0.15 }).observe(hv.closest('.hero'));
    }
  }

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
