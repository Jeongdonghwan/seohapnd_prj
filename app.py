# -*- coding: utf-8 -*-
"""(주)서하P&D 홈페이지 — Flask 라우트. 정적 콘텐츠는 data.py, 문의게시판은 sqlite."""
import hmac
import re
import smtplib
from datetime import datetime
from email.message import EmailMessage
from functools import wraps
try:
    from zoneinfo import ZoneInfo
except ImportError:  # 서버 python 3.8 대비
    from backports.zoneinfo import ZoneInfo

from flask import (Flask, Response, abort, flash, redirect, render_template, request,
                   send_from_directory, session, url_for)
from flask_wtf.csrf import CSRFError, CSRFProtect
from werkzeug.security import check_password_hash, generate_password_hash

import data as D
from config import Config
from db import close_db, get_db

KST = ZoneInfo("Asia/Seoul")
PHONE_RE = re.compile(r"^[0-9\-+() ]{8,20}$")

app = Flask(__name__)
app.config.from_object(Config)
app.teardown_appcontext(close_db)
CSRFProtect(app)
if not Config.SECRET_KEY_SET:
    app.logger.warning("SECRET_KEY 미설정: 재시작·워커마다 세션이 바뀜. 운영에선 .env에 반드시 설정")


# ─── 공통 ───────────────────────────────────────────────

@app.context_processor
def _globals():
    return {"C": D.COMPANY, "NAV": D.NAV, "SITE_URL": app.config["SITE_URL"]}


@app.template_filter("mask")
def mask_name(s):
    """김재홍 → 김*홍, 홍길 → 홍*, 남궁민수 → 남**수"""
    s = (s or "").strip()
    if len(s) < 2:
        return s
    return s[0] + "*" if len(s) == 2 else s[0] + "*" * (len(s) - 2) + s[-1]


@app.template_filter("nl2br")
def nl2br(s):
    from markupsafe import Markup, escape
    return Markup("<br>".join(escape(s or "").split("\n")))


def now_str():
    return datetime.now(KST).strftime("%Y-%m-%d %H:%M")


def client_ip():
    xff = request.headers.get("X-Forwarded-For", "")
    return (xff.split(",")[0].strip() if xff else request.remote_addr or "")[:45]


def admin_required(view):
    @wraps(view)
    def wrapped(*a, **k):
        auth, cfg = request.authorization, app.config
        ok = (auth and cfg["ADMIN_ID"] and cfg["ADMIN_PW"]
              and hmac.compare_digest(auth.username or "", cfg["ADMIN_ID"])
              and hmac.compare_digest(auth.password or "", cfg["ADMIN_PW"]))
        if not ok:
            return Response("", 401, {"WWW-Authenticate": 'Basic realm="seoha admin"'})
        return view(*a, **k)
    return wrapped


def notify(inq):
    """새 문의 메일 알림. SMTP 미설정이면 무시, 실패해도 문의 저장엔 영향 없음."""
    cfg = app.config
    if not (cfg["SMTP_HOST"] and cfg["NOTIFY_TO"]):
        return
    msg = EmailMessage()
    msg["Subject"] = f"[서하P&D 문의] {inq['subject']}"
    msg["From"] = cfg["SMTP_USER"] or cfg["NOTIFY_TO"]
    msg["To"] = cfg["NOTIFY_TO"]
    msg.set_content(f"이름: {inq['name']}\n연락처: {inq['phone']}\n이메일: {inq['email']}\n회사: {inq['company']}\n\n{inq['content']}\n\n"
                    f"답변: {cfg['SITE_URL']}/admin")
    try:
        with smtplib.SMTP(cfg["SMTP_HOST"], cfg["SMTP_PORT"], timeout=10) as s:
            s.starttls()
            if cfg["SMTP_USER"]:
                s.login(cfg["SMTP_USER"], cfg["SMTP_PW"])
            s.send_message(msg)
    except Exception as e:  # ponytail: 알림 실패는 로그만
        app.logger.warning("notify failed: %s", e)


# ─── 정적 페이지 ─────────────────────────────────────────

@app.route("/")
def home():
    return render_template("home.html", products=D.PRODUCTS, certs=D.CERTS,
                           bio=D.PRODUCT_MAP["eroun-bio"], factory=D.FACTORY[:3])


@app.route("/about")
def about():
    return render_template("about.html", org=D.ORG, certs=D.CERTS)


@app.route("/products")
def products():
    return render_template("products.html", products=D.PRODUCTS)


@app.route("/products/<slug>")
def product(slug):
    p = D.PRODUCT_MAP.get(slug) or abort(404)
    return render_template("product.html", p=p, products=D.PRODUCTS)


@app.route("/spec")
def spec():
    return render_template("spec.html", rows=D.SPEC_ROWS)


@app.route("/certifications")
def certifications():
    return render_template("certifications.html", certs=D.CERTS)


@app.route("/factory")
def factory():
    return render_template("factory.html", photos=D.FACTORY)


@app.route("/brochure.pdf")
def brochure():
    return send_from_directory(app.static_folder, "brochure.pdf", download_name="서하P&D_브로슈어.pdf")


@app.route("/sitemap.xml")
def sitemap():
    base = app.config["SITE_URL"] or request.url_root.rstrip("/")
    urls = ["/", "/about", "/products", "/spec", "/certifications", "/factory", "/inquiry"] + \
           [f"/products/{p['slug']}" for p in D.PRODUCTS]
    body = "".join(f"<url><loc>{base}{u}</loc></url>" for u in urls)
    return Response(f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{body}</urlset>',
                    mimetype="application/xml")


@app.route("/robots.txt")
def robots():
    base = app.config["SITE_URL"] or request.url_root.rstrip("/")
    return Response(f"User-agent: *\nDisallow: /admin\nSitemap: {base}/sitemap.xml\n", mimetype="text/plain")


# ─── 문의게시판 ──────────────────────────────────────────

def remember(iid):
    """이 브라우저가 열람 가능한 비밀글 id. 최근 30개만."""
    session["inq_ok"] = (session.get("inq_ok", []) + [iid])[-30:]


def can_view(inq):
    return not inq["is_private"] or inq["id"] in session.get("inq_ok", [])


@app.route("/inquiry")
def inquiry():
    page = max(1, request.args.get("page", 1, type=int))
    per = app.config["PER_PAGE"]
    db = get_db()
    total = db.execute("SELECT COUNT(*) FROM inquiries").fetchone()[0]
    rows = db.execute("SELECT id, name, subject, is_private, status, created_at FROM inquiries ORDER BY id DESC LIMIT ? OFFSET ?",
                      (per, (page - 1) * per)).fetchall()
    return render_template("inquiry.html", rows=rows, page=page, pages=max(1, -(-total // per)), total=total)


@app.route("/inquiry/write", methods=["GET", "POST"])
def inquiry_write():
    if request.method == "GET":
        return render_template("inquiry_write.html", f={})
    f = {k: request.form.get(k, "").strip() for k in ("name", "phone", "email", "company", "subject", "content", "password")}
    f["is_private"] = 1 if request.form.get("is_private") else 0
    if request.form.get("website"):  # honeypot
        return redirect(url_for("inquiry"))
    err = None
    if not (2 <= len(f["name"]) <= 20):
        err = "이름을 입력해 주세요 (2~20자)"
    elif not PHONE_RE.match(f["phone"]):
        err = "연락처를 확인해 주세요"
    elif not (2 <= len(f["subject"]) <= 100):
        err = "제목을 입력해 주세요 (2~100자)"
    elif not (5 <= len(f["content"]) <= 3000):
        err = "내용을 입력해 주세요 (5~3000자)"
    elif f["is_private"] and not (4 <= len(f["password"]) <= 20):
        err = "비밀글 비밀번호는 4자 이상 입력해 주세요"
    if err:
        flash(err)
        return render_template("inquiry_write.html", f=f), 400
    db = get_db()
    cur = db.execute(
        "INSERT INTO inquiries(name, phone, email, company, subject, content, is_private, pw_hash, created_at, ip) VALUES(?,?,?,?,?,?,?,?,?,?)",
        (f["name"], f["phone"], f["email"][:100], f["company"][:50], f["subject"], f["content"], f["is_private"],
         generate_password_hash(f["password"]) if f["is_private"] else "", now_str(), client_ip()))
    db.commit()
    remember(cur.lastrowid)
    notify(f)
    flash("문의가 접수되었습니다. 확인 후 답변 드리겠습니다.")
    return redirect(url_for("inquiry_view", iid=cur.lastrowid))


@app.route("/inquiry/<int:iid>", methods=["GET", "POST"])
def inquiry_view(iid):
    inq = get_db().execute("SELECT * FROM inquiries WHERE id=?", (iid,)).fetchone() or abort(404)
    if request.method == "POST":
        if check_password_hash(inq["pw_hash"], request.form.get("password", "")):
            remember(iid)
            return redirect(url_for("inquiry_view", iid=iid))
        flash("비밀번호가 맞지 않습니다")
    return render_template("inquiry_view.html", inq=inq, ok=can_view(inq))


# ─── 관리자 ─────────────────────────────────────────────

@app.route("/admin")
@admin_required
def admin():
    status = request.args.get("status")
    db = get_db()
    where, args = ("WHERE status=?", (int(status),)) if status in ("0", "1") else ("", ())
    rows = db.execute(f"SELECT * FROM inquiries {where} ORDER BY status, id DESC LIMIT 300", args).fetchall()
    pending = db.execute("SELECT COUNT(*) FROM inquiries WHERE status=0").fetchone()[0]
    return render_template("admin/inquiries.html", rows=rows, status=status, pending=pending)


@app.route("/admin/inquiry/<int:iid>", methods=["GET", "POST"])
@admin_required
def admin_inquiry(iid):
    db = get_db()
    inq = db.execute("SELECT * FROM inquiries WHERE id=?", (iid,)).fetchone() or abort(404)
    if request.method == "POST":
        if request.form.get("action") == "delete":
            db.execute("DELETE FROM inquiries WHERE id=?", (iid,))
            db.commit()
            flash(f"#{iid} 삭제됨")
            return redirect(url_for("admin"))
        answer = request.form.get("answer", "").strip()
        db.execute("UPDATE inquiries SET answer=?, status=?, answered_at=? WHERE id=?",
                   (answer, 1 if answer else 0, now_str() if answer else None, iid))
        db.commit()
        flash("답변 저장됨" if answer else "답변 비움 (대기 상태로)")
        return redirect(url_for("admin_inquiry", iid=iid))
    return render_template("admin/inquiry.html", inq=inq)


@app.errorhandler(CSRFError)
def csrf_error(_):
    flash("페이지가 오래되어 다시 시도해 주세요.")
    return redirect(request.referrer or url_for("home"))


@app.errorhandler(404)
def not_found(_):
    return render_template("404.html"), 404


if __name__ == "__main__":
    app.run(debug=True, port=5001)
