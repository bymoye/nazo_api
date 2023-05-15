import os
import sqlite3
import orjson
from dataclass import IPDataClass, QQDataClass
from typing import Optional, Union


class SelfSqlite:
    def __init__(self) -> None:
        # self.con = sqlite3.connect(":memory:")
        self.con = sqlite3.connect("backup_db.db")
        self.con.row_factory = sqlite3.Row
        # if os.path.exists("backup_db.db"):
        #     with sqlite3.connect("backup_db.db") as db:
        #         db.backup(self.con)
        self.create_ip_table()
        self.create_qq_table()

    def close(self) -> None:
        # with sqlite3.connect("backup_db.db") as db:
        #     self.con.backup(db)
        self.con.close()

    def create_ip_table(self) -> None:
        try:
            create_table = """
            CREATE TABLE IF NOT EXISTS ip_cache(
            ip            TEXT,
            result        TEXT,
            create_time    TIMESTAMP,
            PRIMARY KEY (ip),
            UNIQUE (ip)
            );
            """
            with self.con as con:
                con.execute(create_table)
        except:
            raise Exception("创建IP缓存表发生错误")

    def create_qq_table(self) -> None:
        try:
            create_table = """
            CREATE TABLE IF NOT EXISTS qq_cache(
            qq_number       CHAR(15),
            result      TEXT,
            create_time  TIMESTAMP,
            PRIMARY KEY (qq_number),
            UNIQUE      (qq_number)
            );
            """
            with self.con as con:
                con.execute(create_table)
        except:
            raise Exception("创建QQ缓存表发生错误")

    def query_qq_table(self, qqnum: str) -> Optional[QQDataClass]:
        sql = "select * FROM qq_cache WHERE qq_number=:qqnum AND create_time > strftime('%s','now') - 43200"
        with self.con as con:
            result = con.execute(sql, {"qqnum": qqnum}).fetchone()
            return (
                None
                if result is None
                else QQDataClass(**orjson.loads(result["result"]))
            )

    def query_ip_table(self, ip: str) -> Union[IPDataClass, bool]:
        sql = "select * FROM ip_cache WHERE ip=:ip AND create_time > strftime('%s','now') - 2592000"
        with self.con as con:
            result = con.execute(sql, {"ip": ip}).fetchone()
            return (
                False
                if result is None
                else IPDataClass(**orjson.loads(result["result"]))
            )

    def write_qq_table(self, qqnum: str, result: QQDataClass) -> None:
        sql = "INSERT OR REPLACE INTO qq_cache VALUES (:qqnum , :result , strftime('%s','now'))"
        with self.con as con:
            con.execute(sql, {"qqnum": qqnum, "result": orjson.dumps(result)})

    def write_ip_table(self, ip: str, result: IPDataClass) -> None:
        sql = "INSERT OR REPLACE INTO ip_cache VALUES (:ip , :result , strftime('%s','now'))"
        with self.con as con:
            con.execute(sql, {"ip": ip, "result": orjson.dumps(result)})
