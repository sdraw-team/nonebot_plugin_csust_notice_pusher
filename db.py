import sqlite3
import os
from .notice import Notice
from typing import Any
from nonebot.log import logger


class CachedNotice(object):
    def __init__(self, db_path: str) -> None:
        self.engine = None
        self.db_path = db_path
        self.connect()
        self.init_table()

    def __del__(self):
        self.engine.close()

    def connect(self):
        self.engine = sqlite3.connect(self.db_path)

    def init_table(self):
        cur = self.engine.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS notices (
    id BIGINT PRIMARY KEY,
    url TEXT NOT NULL DEFAULT '',
    title TEXT NOT NULL DEFAULT '',
    content_preview TEXT NOT NULL DEFAULT '',
    publish_date DATE NOT NULL DEFAULT '',
    content TEXT NOT NULL DEFAULT '',
    source TEXT NOT NULL DEFAULT ''
);""")
        self.engine.commit()
        cur.close()

    def get_notice_by_id(self, id: int) -> Notice:
        cur = self.engine.cursor()
        cur.execute(
            f"""SELECT id, url, title, content_preview, publish_date, content, source FROM notices WHERE id = {id}""")
        data = cur.fetchone()
        cur.close()

        if data:
            return Notice(*data)
        else:
            return None

    def is_notice_exists(self, notice_id: int) -> bool:
        res = self.get_notice_by_id(notice_id)
        if res:
            return True
        else:
            return False

    def add_notice(self, data: Notice):
        if self.is_notice_exists(data.id):
            return

        cur = self.engine.cursor()
        sql = """INSERT INTO notices (id, url, title, content_preview, publish_date, content, source)
VALUES ({}, '{}', '{}', '{}', '{}', '{}', '{}');""".format(*map(quote_escape, data.get_properties()))
        cur.execute(sql)
        self.engine.commit()
        cur.close()


def quote_escape(x: str | Any):
    if isinstance(x, str):
        x = x.replace("'", "''")
    return x
