import sqlite3
import os
from dataclass import Ip_info,Qq_info
import orjson
class sqlite:
    def __init__(self) -> None:
        self.con = sqlite3.connect(":memory:")
        self.con.row_factory = sqlite3.Row
        if os.path.exists('backup_db.db'):
            with sqlite3.connect('backup_db.db') as db:
                db.backup(self.con)
        self.Create_IP_Table()
        self.Create_QQ_Table()

    def close(self) -> None:
        with sqlite3.connect('backup_db.db') as db:
            self.con.backup(db)
        self.con.close()

    def Create_IP_Table(self) -> None:
        try:
            create_table = '''
            CREATE TABLE IF NOT EXISTS ipcache(
            IP            TEXT,
            Result        TEXT,
            CreateTime    TIMESTAMP,
            PRIMARY KEY (IP),
            UNIQUE (IP)
            );
            '''
            with self.con as con:
                con.execute(create_table)
        except:
            raise Exception('创建IP缓存表发生错误')
    
    def Create_QQ_Table(self) -> None:
        try:
            create_table = '''
            CREATE TABLE IF NOT EXISTS qqcache(
            qqnum       INT,
            Result      TEXT,
            CreateTime  TIMESTAMP,
            PRIMARY KEY (qqnum),
            UNIQUE      (qqnum)
            );
            '''
            with self.con as con:
                con.execute(create_table)
        except:
            raise Exception('创建QQ缓存表发生错误')

    def Query_Qq_Table(self, qqnum:int) -> Qq_info|bool:
        sql = "select * FROM qqcache WHERE qqnum=:qqnum AND CreateTime > strftime('%s','now') - 43200"
        with self.con as con:
            result = con.execute(sql,{'qqnum':qqnum}).fetchone()
            return False if result is None else Qq_info(**orjson.loads(result['Result']))

    def Query_Ip_Table(self, IP:str) -> Ip_info|bool:
        sql = "select * FROM ipcache WHERE IP=:IP AND CreateTime > strftime('%s','now') - 2592000"
        with self.con as con:
            result = con.execute(sql,{'IP':IP}).fetchone()
            return False if result is None else Ip_info(**orjson.loads(result['Result']))
    
    def Write_Qq_Table(self,qqnum:int,Result:Qq_info) -> None:
        sql = "INSERT OR REPLACE INTO qqcache VALUES (:qqnum , :Result , strftime('%s','now'))"
        with self.con as con:
            con.execute(sql,{'qqnum':qqnum,'Result':orjson.dumps(Result)})

    def Write_Ip_Table(self,IP:str,Result:Ip_info) -> None:
        sql = "INSERT OR REPLACE INTO ipcache VALUES (:IP , :Result , strftime('%s','now'))"
        with self.con as con:
            con.execute(sql,{'IP':IP,'Result':orjson.dumps(Result)})