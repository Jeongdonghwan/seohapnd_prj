# -*- coding: utf-8 -*-
"""스모크: 전체 라우트·링크 + 문의게시판 + 관리자 전 기능. 실행: python -X utf8 test_smoke.py"""
import os
import re
import tempfile

os.environ["DB_PATH"] = os.path.join(tempfile.mkdtemp(), "t.db")
os.environ["ADMIN_ID"], os.environ["ADMIN_PW"] = "adm", "pw"

from app import app  # noqa: E402
import data as D  # noqa: E402

app.config.update(WTF_CSRF_ENABLED=False, DB_PATH=os.environ["DB_PATH"], ADMIN_ID="adm", ADMIN_PW="pw")
AUTH = {"Authorization": "Basic YWRtOnB3"}       # adm:pw
BAD = {"Authorization": "Basic YWRtOnh4"}        # adm:xx


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
    for u in ("/sitemap.xml", "/robots.txt", "/brochure.pdf", "/static/img/og.jpg"):
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

    # 6. 관리자 인증
    assert c.get("/admin").status_code == 401
    assert c.get("/admin", headers=BAD).status_code == 401
    assert c.get("/admin/inquiry/1").status_code == 401
    assert c.post("/admin/inquiry/1", data={"answer": "x"}).status_code == 401
    assert c.post("/admin/inquiry/1", data={"action": "delete"}, headers=BAD).status_code == 401
    assert c.get("/inquiry/1").status_code == 200                                # 무단 삭제 안 됨

    # 7. 관리자 목록·필터
    a = c.get("/admin", headers=AUTH).get_data(as_text=True)
    assert "010-1234-5678" in a and "김재홍" in a                                 # 관리자는 실명·연락처
    assert "답변대기 <b>17</b>" in a
    assert c.get("/admin?status=1", headers=AUTH).get_data(as_text=True).count('class="status s1"') == 0
    assert c.get("/admin?status=x", headers=AUTH).status_code == 200

    # 8. 관리자 상세 → 비밀글도 열람, 답변 저장·수정·비우기
    d = c.get("/admin/inquiry/1", headers=AUTH).get_data(as_text=True)
    assert "흑색 LD 견적" in d and "비밀글" in d and "&lt;script&gt;" in d
    c.post("/admin/inquiry/1", data={"answer": "견적서 보내드렸습니다"}, headers=AUTH)
    v = c.get("/inquiry/1").get_data(as_text=True)
    assert "견적서 보내드렸습니다" in v and "답변완료" in v
    assert "답변완료" in c.get("/inquiry?page=2").get_data(as_text=True)    # #1은 2페이지
    assert "답변대기 <b>16</b>" in c.get("/admin", headers=AUTH).get_data(as_text=True)
    assert "흑색 LD 견적" in c.get("/admin?status=1", headers=AUTH).get_data(as_text=True)
    assert "흑색 LD 견적" not in c.get("/admin?status=0", headers=AUTH).get_data(as_text=True)
    c.post("/admin/inquiry/1", data={"answer": "수정된 답변"}, headers=AUTH)
    assert "수정된 답변" in c.get("/inquiry/1").get_data(as_text=True)
    c.post("/admin/inquiry/1", data={"answer": "  "}, headers=AUTH)               # 비우면 대기로 복귀
    v = c.get("/inquiry/1").get_data(as_text=True)
    assert "답변대기" in v and "수정된 답변" not in v
    assert c.get("/admin/inquiry/999", headers=AUTH).status_code == 404

    # 9. 삭제
    r = c.post("/admin/inquiry/2", data={"action": "delete"}, headers=AUTH)
    assert r.status_code == 302 and c.get("/inquiry/2").status_code == 404
    assert "공개 문의" not in c.get("/admin", headers=AUTH).get_data(as_text=True)

    # 10. CSRF: 토큰 없는 POST는 거부되고 저장 안 됨
    app.config["WTF_CSRF_ENABLED"] = True
    try:
        c3 = app.test_client()
        r = c3.post("/inquiry/write", data={"name": "홍길동", "phone": "010-1234-5678", "subject": "CSRF 테스트", "content": "토큰 없이 보냄"})
        assert r.status_code == 302
        assert "CSRF 테스트" not in c3.get("/admin", headers=AUTH).get_data(as_text=True)
        r = c3.post("/admin/inquiry/1", data={"action": "delete"}, headers=AUTH)
        assert r.status_code == 302 and c3.get("/inquiry/1").status_code == 200
    finally:
        app.config["WTF_CSRF_ENABLED"] = False

    # 11. 마스킹 필터
    m = app.jinja_env.filters["mask"]
    assert (m("김재홍"), m("홍길"), m("남궁민수"), m("A")) == ("김*홍", "홍*", "남**수", "A")
    print("smoke ok")


if __name__ == "__main__":
    main()
