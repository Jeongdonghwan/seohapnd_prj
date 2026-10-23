# (주)서하P&D 홈페이지 — CLAUDE.md

담양 농업용 멀칭필름 제조사 기업 사이트. 벤치마크 ghouse.kr(일신하이폴리), 스택·톤은 walga_prj 승계.
계획·진행 기록·미확정 사항은 `PLAN.md`.

## 스택
- Flask + Jinja2 SSR, 바닐라 JS 1파일(`static/app.js`), CSS 1파일(`static/style.css`), Pretendard CDN
- 콘텐츠(회사정보·제품 8종·규격표·인증 9건·조직도·사진 캡션)는 전부 `data.py`. 문구 수정은 여기만
- 문의게시판만 SQLite(`db.py`, 테이블 1개 `inquiries`, 첫 연결 시 자동 생성). 파일 경로 `DB_PATH`(기본 `inquiries.db`)
- 관리자 `/admin`: BasicAuth(`ADMIN_ID`/`ADMIN_PW` in `.env`). 문의 답변·삭제만 있음, 공지사항 없음
- 새 문의 메일 알림은 `SMTP_HOST`+`NOTIFY_TO` 설정 시에만. 실패해도 문의 저장엔 영향 없음
- CSRF: Flask-WTF `CSRFProtect`. 폼에 `csrf_token` hidden 필수. 스팸은 허니팟 필드 `website`

## 디자인 규칙 (2026-10-14 사용자 확정)
- 컬러: 팜플렛 블루 `--brand:#2F7BFF`, 네이비 `--navy:#0B1F3A`, 생분해 전용 그린 `--green:#2FA84F`
- 로고: 원본 `서하피엔디 로고.ai` → `tools/build_logo.py`로 `static/img/logo/` SVG 생성 (2026-10-19). 헤더 `logo-h.svg`(홈 히어로 위·메뉴 열림은 `logo-h-white.svg`), 인트로·푸터 `logo-white.svg`, 파비콘은 로고 파랑 둥근 사각형+흰 S 마크(`static/favicon.svg`·`favicon.ico`(/favicon.ico 라우트)·`apple-touch-icon.png`). 로고 글자색 #036EB7. **'용표' 배지·문구는 쓰지 않음**
- 홈에 숫자 카운트(설립연도 등) 띠 넣지 않음 (제거됨). 제품은 4×2 그리드, 가로 스크롤 아님
- **알약형 라벨(.tag) 쓰지 않음** ("AI 같다"는 이유로 제거, 2026-10-18). 섹션 소제목(eyebrow)은 영문 대문자 말고 한글
- 모션: CSS + IntersectionObserver `.reveal` 하나. 라이브러리 금지. `prefers-reduced-motion` 시 전부 꺼짐
- 인트로(스플래시) 1.5초는 메인 화면에서만, 새로고침·모바일 포함 매번 표시 (2026-10-18 요청). 서브 페이지엔 없음
- 히어로 영상: 원본 `서하피엔디 ver 1.5.mp4`(30초)에서 0~23.4초(밭 장면, 끝의 공장+로고 자막 제외)만 무음으로 잘라 `static/video/hero-pc.mp4`(1920×1080)·`hero-mobile.mp4`(가운데 세로 크롭 720×1280)+첫 프레임 jpg. 세로 화면이면 모바일용 (app.js), 동작 줄이기면 사진만
- 서브 페이지 상단은 `templates/_page.html`의 `phead()` 매크로

## 실행·검증
```
python app.py            # http://127.0.0.1:5001 (debug, 자동 리로드)
python -X utf8 test_smoke.py   # 전체 라우트·내부 링크 + 문의(검증·허니팟·비밀글·XSS·페이징) + 관리자(인증·필터·답변 저장/수정/비우기·삭제) + CSRF
python -I -X utf8 tools/optimize_images.py "<자료 폴더>"   # 원본 → static/img WebP, brochure.pdf (1회성)
```
- Windows에서 서버 여러 개가 같은 포트에 겹쳐 뜰 수 있음. 재시작 전 5001 포트의 `app.py` 프로세스(부모·자식)를 모두 죽일 것

## 배포 (Phase 5, 미완)
- Cafe24 멀티사이트, Gunicorn + Nginx. `/deploy` 스킬 사용. `.env`에 `SITE_URL`, `SECRET_KEY`, `ADMIN_*` 필수
