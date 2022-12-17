from base64 import encode
from blacksheep.client.session import ClientSession
from modules.sql_todo import SelfSqlite
from dataclass import Qq_info
import orjson, httpx


class QQUtils:
    def __init__(self, client: ClientSession, sql: SelfSqlite) -> None:
        self.sql = sql
        self.flag = {}

    def Error(self, msg: str, qqnum: str | None = None, clear: bool = False) -> None:
        if clear:
            self.flag.pop(qqnum)
        raise Exception(msg)

    async def get_qqinfo(self, qqnum: int) -> Qq_info:
        if qq_info := self.sql.query_qq_table(qqnum):
            return qq_info
        qqnum = str(qqnum)
        if self.flag.get(qqnum):
            return "当前QQ正在获取,请勿重复请求"
        self.flag[qqnum] = 1
        # self.Error("当前QQ正在获取,请勿重复请求")
        async with httpx.AsyncClient(
            follow_redirects=False, default_encoding="GBK"
        ) as client:
            req = [
                await client.get(
                    f"https://r.qzone.qq.com/fcg-bin/cgi_get_portrait.fcg?g_tk=1518561325&uins={qqnum}"
                ),
                await client.get(
                    f"https://s.p.qq.com/pub/get_face?img_type=5&uin={qqnum}"
                ),
            ]
        if req[0].status_code != 200 or req[1].status_code != 302:
            self.Error("请求错误", qqnum, True)
        nickname_api = req[0].text
        qqavatar_api = req[1].headers.get("Location")
        nickname_begin = "portraitCallBack("
        jsonp_end = ")"
        if not nickname_api.startswith(nickname_begin) or not nickname_api.endswith(
            jsonp_end
        ):
            self.Error("接口内容错误", qqnum, True)
        nickname = orjson.loads(nickname_api[len(nickname_begin) : -len(jsonp_end)])
        if qqnum not in nickname:
            self.Error("返回的结果中号码不匹配,可能号码不存在", qqnum, True)
        result = Qq_info(qqnum, nickname[qqnum][6], qqavatar_api)
        self.sql.write_qq_table(int(qqnum), result)
        self.flag.pop(qqnum)
        return result
