import grequests
from fastapi import APIRouter,status, Path, Query
from fastapi.responses import ORJSONResponse
import orjson
import ast
from modules.qqsql import qqcache
router = APIRouter()
qqcl = qqcache()
@router.get("/{qqnum}",description="仅接受5-10位QQ号(且仅为数字)")
async def get_qqinfo(qqnum: int = Path(..., ge=10000, le=10000000000)):
    cache_slc = qqcl._get_cache(qqnum,True)
    if cache_slc != 0:
            c = ast.literal_eval(cache_slc[1])
            result = {"qqnumber": c['qqnumber'],
            "qqname": c['qqname'],
            "qqavatar": c['qqavatar']}
            headers = {'X-expires': str(cache_slc[2])}
    else:
        qqnum = str(qqnum)
        req_list = [grequests.get("https://r.qzone.qq.com/fcg-bin/cgi_get_portrait.fcg?g_tk=1518561325&uins="+qqnum),
                    grequests.get("https://s.p.qq.com/pub/get_face?img_type=3&uin="+qqnum, allow_redirects=False)]
        res_list = grequests.map(req_list)
        res_list[0].encoding = 'GBK'
        nickname_api = res_list[0].text
        qqavatar_api = res_list[1].headers
        nickname_begin = r'portraitCallBack('
        jsonp_end = r')'
        # 判断是否返回获取正确的jsonp格式
        if not nickname_api.startswith(nickname_begin) or \
                not nickname_api.endswith(jsonp_end):
            return ORJSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content='获取失败,检查是否正确.')
        # jsonp转json并解析
        nickname = orjson.loads(nickname_api[len(nickname_begin):-len(jsonp_end)])
        # 判断返回的json中是否包括QQ号 QQAPI 很奇怪的地方是 错误的QQ号可能会返回其他的QQ号？
        if not qqnum in nickname:
            return ORJSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content='qq号码或许不存在.')
        # QQ头像
        qqavatar = qqavatar_api['Location']
        # 返回值
        result = {"qqnumber": qqnum,
                "qqname": nickname[qqnum][6],
                "qqavatar": qqavatar}
        # 写入sqlite 做缓存 (12h)
        qqcl._write_cache(int(qqnum),str(result))
    # 头, 分别为 缓存创建时间 缓存过期时间(避免短时间内重复爬取 以缩短时间)
        headers = {'X-expires': 'Nocache'}
    return ORJSONResponse(status_code=status.HTTP_200_OK, content=result,headers = headers)
