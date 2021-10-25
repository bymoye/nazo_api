from blacksheep.client.session import ClientSession
from modules.sql_todo import sqlite
from dataclass import Qq_info
import orjson
class _qq:
    def __init__(self,client:ClientSession,sql:sqlite) -> None:
        self.client , self.sql = client, sql
        
    async def Get_qqinfo(self,qqnum:int) -> Qq_info:
        Qqinfo = await self.sql.Query_Qq_Table(qqnum)
        if Qqinfo:
            result = Qqinfo
        else:
            qqnum = str(qqnum)
            req = [await self.client.get("https://r.qzone.qq.com/fcg-bin/cgi_get_portrait.fcg?g_tk=1518561325&uins="+qqnum),
                    await self.client.get("https://s.p.qq.com/pub/get_face?img_type=5&uin="+qqnum)
                    ]
            assert (req[0] is not None and req[1] is not None),'请求错误'
            nickname_api = await req[0].text()
            nickname_api = nickname_api.encode("iso-8859-1").decode('GB18030')
            qqavatar_api = bytes.decode(req[1].get_headers(b"Location")[0])
            nickname_begin = r'portraitCallBack('
            jsonp_end = r')'
            assert (nickname_api.startswith(nickname_begin) and nickname_api.endswith(jsonp_end)),'接口内容错误'
            nickname = orjson.loads(nickname_api[len(nickname_begin):-len(jsonp_end)])
            assert (qqnum in nickname),'返回的结果中号码不匹配,可能号码不存在'
            result = Qq_info(
                            qqnum,
                            nickname[qqnum][6],
                            qqavatar_api
                        )
            await self.sql.Write_Qq_Table(int(qqnum),result)
        return result