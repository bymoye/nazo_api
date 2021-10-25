import aiosqlite
import os
from dataclass import Ip_info,Qq_info
import orjson
class sqlite:
    def __init__(self) -> None:
        ...

    async def init(self) -> None:
        self.con = await aiosqlite.connect(":memory:")
        self.con.row_factory = aiosqlite.Row
        if os.path.exists('backup_db.db'):
            async with aiosqlite.connect('backup_db.db') as db:
                await db.backup(self.con)
        await self.Create_IP_Table()
        await self.Create_QQ_Table()

    async def close(self) -> None:
        async with aiosqlite.connect('backup_db.db') as db:
            await self.con.backup(db)
        await self.con.close()

    async def Create_IP_Table(self) -> None:
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
            await self.con.execute(create_table)
            await self.con.commit()
        except:
            raise Exception('创建IP缓存表发生错误')
    
    async def Create_QQ_Table(self) -> None:
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
            await self.con.execute(create_table)
            await self.con.commit()
        except:
            raise Exception('创建QQ缓存表发生错误')

    async def Query_Qq_Table(self, qqnum:int) -> Qq_info|bool:
        sql = "select * FROM qqcache WHERE qqnum=:qqnum AND CreateTime > strftime('%s','now') - 43200"
        result = await self.con.execute(sql,{'qqnum':qqnum})
        result = await result.fetchone()
        return False if result is None else Qq_info(**orjson.loads(result['Result']))

    async def Query_Ip_Table(self, IP:str) -> Ip_info|bool:
        sql = "select * FROM ipcache WHERE IP=:IP AND CreateTime > strftime('%s','now') - 2592000"
        result = await self.con.execute(sql,{'IP':IP})
        result = await result.fetchone()
        return False if result is None else Ip_info(**orjson.loads(result['Result']))
    
    async def Write_Qq_Table(self,qqnum:int,Result:Qq_info) -> None:
        sql = "INSERT OR REPLACE INTO qqcache VALUES (:qqnum , :Result , strftime('%s','now'))"
        await self.con.execute(sql,{'qqnum':qqnum,'Result':orjson.dumps(Result)})
        await self.con.commit()

    async def Write_Ip_Table(self,IP:str,Result:Ip_info) -> None:
        sql = "INSERT OR REPLACE INTO ipcache VALUES (:IP , :Result , strftime('%s','now'))"
        await self.con.execute(sql,{'IP':IP,'Result':orjson.dumps(Result)})
        await self.con.commit()