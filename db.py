# -*- coding: utf-8 -*-
"""문의게시판 SQLite. 테이블 1개, 첫 연결 시 생성."""
import sqlite3

from flask import current_app, g

SCHEMA = """CREATE TABLE IF NOT EXISTS inquiries(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL, phone TEXT NOT NULL, email TEXT NOT NULL DEFAULT '', company TEXT NOT NULL DEFAULT '',
  subject TEXT NOT NULL, content TEXT NOT NULL,
  is_private INTEGER NOT NULL DEFAULT 1, pw_hash TEXT NOT NULL DEFAULT '',
  status INTEGER NOT NULL DEFAULT 0, answer TEXT NOT NULL DEFAULT '', answered_at TEXT,
  created_at TEXT NOT NULL, ip TEXT NOT NULL DEFAULT ''
)"""


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(current_app.config["DB_PATH"])
        g.db.row_factory = sqlite3.Row
        g.db.execute(SCHEMA)
    return g.db


def close_db(_=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()
