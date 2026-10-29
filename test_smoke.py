# -*- coding: utf-8 -*-
"""스모크: 전체 라우트·링크 + 문의게시판 + 관리자 전 기능. 실행: python -X utf8 test_smoke.py"""
import os
import re
import tempfile

os.environ["DB_PATH"] = os.path.join(tempfile.mkdtemp(), "t.db")
os.environ["ADMIN_ID"], os.environ["ADMIN_PW"] = "adm", "pw"

from app import LOGIN_FAILS, app  # noqa: E402
import data as D  # noqa: E402

app.config.update(WTF_CSRF_ENABLED=False, DB_PATH=os.environ["DB_PATH"], ADMIN_ID="adm", ADMIN_PW="pw")


def login(c, pw="pw"):
    return c.post("/admin/login", data={"username": "adm", "password": pw, "next": "/admin"})


def write(c, **kw):
    d = {"name": "홍길동", "phone": "010-1234-5678", "subject": "견적 문의", "content": "폭 150 두께 0.02"}
    d.update(kw)
    return c.post("/inquiry/write", data=d)


def main():
    c = app.test_client()

    # 1. 전체 페이지 200 + 내부 링크·이미지 전부 살아있는지
    pages = ["/", "/about", "/products", "/spec", "/certifications", "/factory", "/inquiry", "/inquiry/write"] + \
            [f"/products/{p['slug']}" for p in D.PRODUCTS]
    seen = set()
    for u in pages:
        r = c.get(u)
        assert r.status_code == 200, u
        html = r.get_data(as_text=True)
        assert html.count("<h1") >= 1, u
        for ref in re.findall(r'(?:href|src|data-img)="(/[^"#?]*)', html):
            if ref not in seen and not ref.startswith("/admin"):
                seen.add(ref)
                assert c.get(ref).status_code == 200, (u, ref)
    for u in ("/sitemap.xml", "/robots.txt", "/brochure.pdf", "/static/img/og.jpg", "/favicon.ico", "/static/favicon.svg"):
        assert c.get(u).status_code == 200, u
    assert all(f"/products/{p['slug']}" in c.get("/sitemap.xml").get_data(as_text=True) for p in D.PRODUCTS)
    assert c.get("/nope").status_code == 404 and c.get("/products/nope").status_code == 404 and c.get("/inquiry/999").status_code == 404

    # 2. 문의 검증·스팸
    assert write(c, name="a").status_code == 400
    assert write(c, phone="abc").status_code == 400
    assert write(c, content="짧").status_code == 400
    assert write(c, is_private="1", password="12").status_code == 400          # 비밀번호 짧음
    r = write(c, name="", subject="입력 유지 확인")
    assert r.status_code == 400 and "입력 유지 확인" in r.get_data(as_text=True)  # 실패 시 입력값 보존
    assert write(c, website="spam").status_code == 302                          # 허니팟: 저장 안 됨
    assert "등록된 문의" not in c.get("/inquiry").get_data(as_text=True)
    assert "첫 문의를 남겨주세요" in c.get("/inquiry").get_data(as_text=True)

    # 3. 비밀글 (#1) — 작성자 세션 열람, 타인은 비밀번호
    r = write(c, name="김재홍", subject="흑색 LD 견적", content="폭 150 <script>alert(1)</script>\n둘째 줄", is_private="1", password="1234")
    assert r.status_code == 302 and r.headers["Location"].endswith("/inquiry/1")
    html = c.get("/inquiry/1").get_data(as_text=True)
    assert "&lt;script&gt;" in html and "<script>alert" not in html and "<br>둘째 줄" in html   # XSS 이스케이프 + 줄바꿈
    lst = c.get("/inquiry").get_data(as_text=True)
    assert '<td class="who">김*홍</td>' in lst and "답변대기" in lst
    c2 = app.test_client()
    assert "비밀번호를 입력" in c2.get("/inquiry/1").get_data(as_text=True)
    assert "폭 150" not in c2.post("/inquiry/1", data={"password": "0000"}).get_data(as_text=True)
    assert "폭 150" in c2.post("/inquiry/1", data={"password": "1234"}, follow_redirects=True).get_data(as_text=True)

    # 4. 공개글 (#2) — 누구나 열람
    write(c, name="이영희", subject="공개 문의", content="공개 내용입니다")
    assert "공개 내용입니다" in app.test_client().get("/inquiry/2").get_data(as_text=True)

    # 5. 페이징 (#3~#17, 총 17건 / 15건씩 → 2페이지)
    for i in range(15):
        write(c, subject=f"페이징 {i}")
    p1, p2 = c.get("/inquiry").get_data(as_text=True), c.get("/inquiry?page=2").get_data(as_text=True)
    assert 'href="?page=2"' in p1 and "흑색 LD 견적" in p2 and "흑색 LD 견적" not in p1
    assert c.get("/inquiry?page=abc").status_code == 200

    # 6. 관리자 로그인 페이지 (브라우저 팝업 아님)
    r = c.get("/admin")
    assert r.status_code == 302 and "/admin/login" in r.headers["Location"]
    assert "/admin/login" in c.get("/admin/inquiry/1").headers["Location"]
    assert c.post("/admin/inquiry/1", data={"answer": "x"}).status_code == 302
    lp = c.get("/admin/login").get_data(as_text=True)
    assert "관리자 로그인" in lp and 'name="password"' in lp and "WWW-Authenticate" not in str(c.get("/admin").headers)
    bad = app.test_client()
    assert login(bad, "한글비번").status_code == 401                              # 한글 입력에도 500 안 남
    r = login(bad, "xx")
    assert r.status_code == 401 and "맞지 않습니다" in r.get_data(as_text=True)
    assert bad.get("/admin").status_code == 302
    assert c.get("/inquiry/1").status_code == 200                                # 무단 삭제 안 됨
    r = app.test_client().post("/admin/login", data={"username": "adm", "password": "pw", "next": "https://evil.com"})
    assert r.headers["Location"].endswith("/admin")                              # 외부 주소로 안 튕김
    ad = app.test_client()
    r = login(ad)
    assert r.status_code == 302 and r.headers["Location"].endswith("/admin")
    assert ad.get("/admin/login").status_code == 302                             # 로그인 상태면 목록으로

    # 7. 관리자 목록·필터
    a = ad.get("/admin").get_data(as_text=True)
    assert "010-1234-5678" in a and "김재홍" in a                                 # 관리자는 실명·연락처
    assert "답변대기 <b>17</b>" in a
    assert ad.get("/admin?status=1").get_data(as_text=True).count('class="status s1"') == 0
    assert ad.get("/admin?status=x").status_code == 200

    # 8. 관리자 상세 → 비밀글도 열람, 답변 저장·수정·비우기
    d = ad.get("/admin/inquiry/1").get_data(as_text=True)
    assert "흑색 LD 견적" in d and "비밀글" in d and "&lt;script&gt;" in d
    ad.post("/admin/inquiry/1", data={"answer": "견적서 보내드렸습니다"})
    v = c.get("/inquiry/1").get_data(as_text=True)
    assert "견적서 보내드렸습니다" in v and "답변완료" in v
    assert "답변완료" in c.get("/inquiry?page=2").get_data(as_text=True)    # #1은 2페이지
    assert "답변대기 <b>16</b>" in ad.get("/admin").get_data(as_text=True)
    assert "흑색 LD 견적" in ad.get("/admin?status=1").get_data(as_text=True)
    assert "흑색 LD 견적" not in ad.get("/admin?status=0").get_data(as_text=True)
    ad.post("/admin/inquiry/1", data={"answer": "수정된 답변"})
    assert "수정된 답변" in c.get("/inquiry/1").get_data(as_text=True)
    ad.post("/admin/inquiry/1", data={"answer": "  "})               # 비우면 대기로 복귀
    v = c.get("/inquiry/1").get_data(as_text=True)
    assert "답변대기" in v and "수정된 답변" not in v
    assert ad.get("/admin/inquiry/999").status_code == 404

    # 9. 삭제
    r = ad.post("/admin/inquiry/2", data={"action": "delete"})
    assert r.status_code == 302 and c.get("/inquiry/2").status_code == 404
    assert "공개 문의" not in ad.get("/admin").get_data(as_text=True)

    # 10. CSRF: 토큰 없는 POST는 거부되고 저장·삭제 안 됨
    c3 = app.test_client()
    login(c3)
    app.config["WTF_CSRF_ENABLED"] = True
    try:
        r = c3.post("/inquiry/write", data={"name": "홍길동", "phone": "010-1234-5678", "subject": "CSRF 테스트", "content": "토큰 없이 보냄"})
        assert r.status_code == 302
        assert "CSRF 테스트" not in c3.get("/admin").get_data(as_text=True)
        r = c3.post("/admin/inquiry/1", data={"action": "delete"})
        assert r.status_code == 302 and c3.get("/inquiry/1").status_code == 200
        assert c3.post("/admin/logout").status_code == 302 and c3.get("/admin").status_code == 200   # 로그아웃도 토큰 필요
    finally:
        app.config["WTF_CSRF_ENABLED"] = False

    # 10-1. 로그아웃
    assert ad.post("/admin/logout").status_code == 302 and ad.get("/admin").status_code == 302

    # 10-2. 비밀번호 5회 틀리면 10분 잠금 (맞는 비밀번호도 거부)
    lk = app.test_client()
    LOGIN_FAILS.clear()
    for _ in range(5):
        login(lk, "xx")
    r = login(lk)
    assert r.status_code == 401 and "잠겼습니다" in r.get_data(as_text=True)

    # 11. 마스킹 필터
    m = app.jinja_env.filters["mask"]
    assert (m("김재홍"), m("홍길"), m("남궁민수"), m("A")) == ("김*홍", "홍*", "남**수", "A")
    # 12. 영문: 데이터 구조가 국문과 같고, 사전에 빠진 키 없고, 영문 페이지에 한글이 없음
    import glob as _glob
    import data_en as DE
    import i18n
    assert [p["slug"] for p in D.PRODUCTS] == [p["slug"] for p in DE.PRODUCTS]
    assert [c["key"] for c in D.CERTS] == [c["key"] for c in DE.CERTS]
    assert [f["img"] for f in D.FACTORY] == [f["img"] for f in DE.FACTORY]
    assert [k for k, _ in D.NAV] == [k for k, _ in DE.NAV]
    for name in ("SPEC_ROWS", "ORG", "BIO_STEPS", "GREETING", "HISTORY"):
        assert len(getattr(D, name)) == len(getattr(DE, name)), name
    keys = set()
    for tf in _glob.glob("templates/*.html"):
        keys |= {m[1] for m in re.findall(r"""_\((['"])(.*?)\)""", open(tf, encoding="utf-8").read())}
    keys |= set(re.findall(r't\("(.*?)"\)', open("app.py", encoding="utf-8").read()))
    missing = sorted(k for k in keys if k not in i18n.EN)
    assert not missing, missing
    hangul = re.compile(r"[가-힣]")
    e = app.test_client()
    en_pages = ["/en", "/en/", "/en/about", "/en/products", "/en/spec", "/en/certifications", "/en/factory",
                "/en/inquiry/write", "/en/nope"] + [f"/en/products/{p['slug']}" for p in D.PRODUCTS]
    for u in en_pages:
        r = e.get(u)
        assert r.status_code == (404 if u.endswith("nope") else 200), u
        html = re.sub(r"<!--.*?-->", "", r.get_data(as_text=True), flags=re.S)   # 주석은 화면에 안 보임
        assert '<html lang="en"' in html, u
        found = sorted(set(hangul.findall(html)))
        assert not found, (u, "".join(found)[:40], html[html.find(found[0]) - 60:html.find(found[0]) + 40])
        for ref in re.findall(r'href="(/[^"#?]*)', re.sub(r'<[^>]*hreflang="ko"[^>]*>', '', html)):   # KO 전환 버튼 제외           # 영문 페이지 안 링크는 /en 유지 (브로슈어·파비콘·정적 제외)
            if not ref.startswith(("/static", "/brochure.pdf", "/favicon.ico")) and ref not in ("/",):
                assert ref.startswith("/en"), (u, ref)
    # 언어 전환 링크: 같은 페이지의 반대 언어
    ko = c.get("/products/green").get_data(as_text=True)
    assert 'href="/en/products/green"' in ko and '<html lang="ko"' in ko
    en = e.get("/en/products/green").get_data(as_text=True)
    assert 'href="/products/green"' in en and 'hreflang="en"' in en
    assert "/en/products/green" in c.get("/sitemap.xml").get_data(as_text=True)
    assert 'class="lang"' not in ad.get("/admin/login").get_data(as_text=True)    # 관리자는 국문만
    # 영문 문의 작성 → /en 상세로, 영어 안내
    r = e.post("/en/inquiry/write", data={"name": "John", "phone": "+1-555-0100", "subject": "Quote", "content": "Need 100 rolls", "is_private": "1", "password": "abcd"})
    assert r.status_code == 302 and r.headers["Location"].startswith("/en/inquiry/")
    v = e.get(r.headers["Location"]).get_data(as_text=True)
    assert "Your inquiry has been received" in v and "Need 100 rolls" in v and "Pending" in v
    assert "Please enter your name" in e.post("/en/inquiry/write", data={"name": "", "phone": "x", "subject": "s", "content": "c"}).get_data(as_text=True)
    print("smoke ok")


if __name__ == "__main__":
    main()
