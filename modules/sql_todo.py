import sqlite3
import os
from dataclass import IPDataClass, QQDataClass
import orjson


class SelfSqlite:
    def __init__(self) -> None:
        self.con = sqlite3.connect(":memory:")
        self.con.row_factory = sqlite3.Row
        if os.path.exists("backup_db.db"):
            with sqlite3.connect("backup_db.db") as db:
                db.backup(self.con)
        self.create_ip_table()
        self.create_qq_table()

    def close(self) -> None:
        with sqlite3.connect("backup_db.db") as db:
            self.con.backup(db)
        self.con.close()

    def create_ip_table(self) -> None:
        try:
            create_table = """
            CREATE TABLE IF NOT EXISTS ipcache(
            IP            TEXT,
            Result        TEXT,
            CreateTime    TIMESTAMP,
            PRIMARY KEY (IP),
            UNIQUE (IP)
            );
            """
            with self.con as con:
                con.execute(create_table)
        except:
            raise Exception("创建IP缓存表发生错误")

    def create_qq_table(self) -> None:
        try:
            create_table = """
            CREATE TABLE IF NOT EXISTS qqcache(
            qqnum       CHAR(15),
            Result      TEXT,
            CreateTime  TIMESTAMP,
            PRIMARY KEY (qqnum),
            UNIQUE      (qqnum)
            );
            """
            with self.con as con:
                con.execute(create_table)
        except:
            raise Exception("创建QQ缓存表发生错误")

    def query_qq_table(self, qqnum: str) -> QQDataClass | bool:
        sql = "select * FROM qqcache WHERE qqnum=:qqnum AND CreateTime > strftime('%s','now') - 43200"
        with self.con as con:
            result = con.execute(sql, {"qqnum": qqnum}).fetchone()
            return (
                False
                if result is None
                else QQDataClass(**orjson.loads(result["Result"]))
            )

    def query_ip_table(self, IP: str) -> IPDataClass | bool:
        sql = "select * FROM ipcache WHERE IP=:IP AND CreateTime > strftime('%s','now') - 2592000"
        with self.con as con:
            result = con.execute(sql, {"IP": IP}).fetchone()
            return (
                False
                if result is None
                else IPDataClass(**orjson.loads(result["Result"]))
            )

    def write_qq_table(self, qqnum: int, Result: QQDataClass) -> None:
        sql = "INSERT OR REPLACE INTO qqcache VALUES (:qqnum , :Result , strftime('%s','now'))"
        with self.con as con:
            con.execute(sql, {"qqnum": qqnum, "Result": orjson.dumps(Result)})

    def write_ip_table(self, IP: str, Result: IPDataClass) -> None:
        sql = "INSERT OR REPLACE INTO ipcache VALUES (:IP , :Result , strftime('%s','now'))"
        with self.con as con:
            con.execute(sql, {"IP": IP, "Result": orjson.dumps(Result)})
