import orjson, httpx
from modules.sql_todo import SelfSqlite
from dataclass import QQDataClass
from typing import Tuple, Union


class QQUtils:
    def __init__(self, sql: SelfSqlite) -> None:
        self.sql = sql
        self.flag = []

    async def get_qqinfo(self, qqnum: str) -> Tuple[bool, Union[str, QQDataClass]]:
        if qq_info := self.sql.query_qq_table(qqnum):
            return True, qq_info
        if qqnum in self.flag:
            return False, "当前QQ正在获取中,请勿重复请求"
        try:
            self.flag.append(qqnum)
            async with httpx.AsyncClient(
                follow_redirects=False, default_encoding="GBK"
            ) as client:
                nickname_req = await client.get(
                    f"https://r.qzone.qq.com/fcg-bin/cgi_get_portrait.fcg?g_tk=1518561325&uins={qqnum}"
                )
                avatar_req = await client.get(
                    f"https://s.p.qq.com/pub/get_face?img_type=5&uin={qqnum}"
                )
            if nickname_req.status_code != 200 or avatar_req.status_code != 302:
                return False, "请求错误"
            nickname_api = nickname_req.text
            qqavatar_api = avatar_req.headers.get("Location")
            nickname_begin = "portraitCallBack("
            jsonp_end = ")"
            if not nickname_api.startswith(nickname_begin) or not nickname_api.endswith(
                jsonp_end
            ):
                return False, "接口内容错误"
            nickname = orjson.loads(nickname_api[len(nickname_begin) : -len(jsonp_end)])
            if qqnum not in nickname:
                return False, "返回的结果中号码不匹配,可能号码不存在"
            result = QQDataClass(qqnum, nickname[qqnum][6], qqavatar_api)
            self.sql.write_qq_table(result.qq_number, result)
            return True, result
        except Exception as e:
            return False, f"未知错误: {e}"
        finally:
            self.flag.remove(qqnum)
