import sqlite3
import msgspec
from dataclass import IPDataClass
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

    def query_ip_table(self, ip: str) -> Union[IPDataClass, bool]:
        sql = "select * FROM ip_cache WHERE ip=:ip AND create_time > strftime('%s','now') - 2592000"
        with self.con as con:
            result = con.execute(sql, {"ip": ip}).fetchone()
            return (
                False
                if result is None
                else IPDataClass(**msgspec.json.decode(result["result"]))
            )

    def write_ip_table(self, ip: str, result: IPDataClass) -> None:
        sql = "INSERT OR REPLACE INTO ip_cache VALUES (:ip , :result , strftime('%s','now'))"
        with self.con as con:
            con.execute(sql, {"ip": ip, "result": msgspec.json.encode(result)})
