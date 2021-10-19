import sqlite3
from sqlite3.dbapi2 import IntegrityError
import time
class qqcache:
    def __init__(self) -> None:
        self.con = sqlite3.connect('cache.db')
        self.cur = self.con.cursor()
        self._create_table()

    def _create_table(self):  
        try:
            create_table = '''
            CREATE TABLE IF NOT EXISTS qqcache(
            qqnum   INT,
            cont    TEXT,
            exptime TIME,
            PRIMARY KEY (qqnum),
            UNIQUE (qqnum)
            );
            '''
            self.cur.execute(create_table)
        except:
            raise Exception('创建缓存表发生错误')

    def _get_cache(self,qqnum:int, val:bool = False):
        try:
            if val:
                sql ='SELECT * FROM qqcache WHERE qqnum='+ str(qqnum) + ' AND exptime > ' + str(time.time())
            else:
                sql ="SELECT * FROM qqcache WHERE qqnum='{0}'".format(qqnum)
            r = self.con.execute(sql).fetchone()
            return 0 if r is None else r
        except Exception as e:
            raise Exception('查找表发生错误\n' + str(e))

    def _write_cache(self,qqnum:int,cont:str):
        try:
            sql = 'INSERT OR REPLACE INTO qqcache VALUES ({0}, "{1}", {2})'.format(qqnum,cont,int(time.time()+43200))
            self.cur.execute(sql)
            self.con.commit()
        except IntegrityError:
            print("该值已存在")
        except:
            print("插入值失败")
