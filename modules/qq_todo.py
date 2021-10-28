from blacksheep.client.session import ClientSession
from modules.sql_todo import sqlite
from dataclass import Qq_info
import orjson
class _qq:
    def __init__(self,client:ClientSession,sql:sqlite) -> None:
        self.client , self.sql = client, sql
        self.flag = {}
    
    def Error(self,msg:str,qqnum:str|None,clear: bool = False) -> None:
        if clear:
            self.flag.pop(qqnum)
        raise Exception(msg)
    
    async def Get_qqinfo(self,qqnum:int) -> Qq_info:
        Qqinfo = self.sql.Query_Qq_Table(qqnum)
        if Qqinfo:
            result = Qqinfo
        else:
            qqnum = str(qqnum)
            if self.flag.get(qqnum) is None:
                self.flag[qqnum] = 1
            else:
                self.Error('当前QQ正在获取,请勿重复请求')
            req = [await self.client.get("https://r.qzone.qq.com/fcg-bin/cgi_get_portrait.fcg?g_tk=1518561325&uins="+qqnum),
                    await self.client.get("https://s.p.qq.com/pub/get_face?img_type=5&uin="+qqnum)
                    ]
            if req[0] is None or req[1] is None:
                self.Error('请求错误',qqnum,True)
            nickname_api = await req[0].text()
            nickname_api = nickname_api.encode("iso-8859-1").decode('GB18030')
            qqavatar_api = bytes.decode(req[1].get_headers(b"Location")[0])
            nickname_begin = r'portraitCallBack('
            jsonp_end = r')'
            if not nickname_api.startswith(nickname_begin) or not nickname_api.endswith(jsonp_end):
                self.Error('接口内容错误',qqnum,True)
            nickname = orjson.loads(nickname_api[len(nickname_begin):-len(jsonp_end)])
            if qqnum not in nickname:
                self.Error('返回的结果中号码不匹配,可能号码不存在',qqnum,True)
            result = Qq_info(
                            qqnum,
                            nickname[qqnum][6],
                            qqavatar_api
                        )
            self.sql.Write_Qq_Table(int(qqnum),result)
            self.flag.pop(qqnum)
        return result