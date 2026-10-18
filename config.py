# -*- coding: utf-8 -*-
"""환경변수 우선 설정. .env 파일이 있으면 로드한다 (.env.example 참고)."""
import os

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class Config:
    SECRET_KEY_SET = bool(os.environ.get("SECRET_KEY"))
    SECRET_KEY = os.environ.get("SECRET_KEY") or os.urandom(24).hex()
    WTF_CSRF_TIME_LIMIT = None          # 토큰은 세션 수명과 같음 (문의 작성 중 1시간 넘겨도 안 날아가게)
    SESSION_COOKIE_SAMESITE = "Lax"
    SESSION_COOKIE_SECURE = os.environ.get("SITE_URL", "").startswith("https")
    MAX_CONTENT_LENGTH = 1024 * 1024    # 폼 본문 1MB
    SITE_URL = os.environ.get("SITE_URL", "").rstrip("/")
    ADMIN_ID = os.environ.get("ADMIN_ID")
    ADMIN_PW = os.environ.get("ADMIN_PW")
    DB_PATH = os.environ.get("DB_PATH") or os.path.join(BASE_DIR, "inquiries.db")
    # 새 문의 알림 메일 (비워두면 알림 없음)
    SMTP_HOST = os.environ.get("SMTP_HOST", "")
    SMTP_PORT = int(os.environ.get("SMTP_PORT", "587"))
    SMTP_USER = os.environ.get("SMTP_USER", "")
    SMTP_PW = os.environ.get("SMTP_PW", "")
    NOTIFY_TO = os.environ.get("NOTIFY_TO", "")
    PER_PAGE = 15
