from blacksheep import Content
from blacksheep.messages import Request, Response
from blacksheep.server.bindings import ServerInfo
from blacksheep.server.routing import Router
from blacksheep.server.responses import redirect, html, bad_request,not_found
import orjson
from modules.ip_todo import Ip
from modules.qq_todo import _qq
from modules.yiyan_todo import Hitokoto
from modules.rand.randimg import Randimg as rdimg
from dataclass import Get_ua_result,Ip_result,Qq_info,randimg_result,config
from app.docs import UA_API_docs, ip_API_docs,docs, randimg_API_docs, yiyan_API_docs,QQ_API_docs
from app.jsonres import json,pretty_json
from app.services import service
from config import _ApiConfig
router = Router()
get = router.get
add_get = router.add_get
Config:_ApiConfig = service.build_provider().get(config).config.module

# 未定义路由
def fallback() -> Response:
    return json(status=404,data={"msg":"这里不是你该来的地方"})
router.fallback = fallback


@docs.ignore()
@get("/")
async def index():
    return redirect("/docs")

@docs(ip_API_docs)
async def get_ip(ipinfo: Ip, ip: bytes) -> Response:
    print(ip)
    try:
        return json(await ipinfo.get_ip(ip))
    except Exception as e:
        return Response(status=500, content=Content(b"application/json", orjson.dumps({"status": 500, "error": f"{e}"})))

@docs(UA_API_docs)
async def get_ua(request: Request,ip:ServerInfo,ipinfo: Ip) -> Response:
    header = dict([(i.decode(),j.decode()) for i,j in request.headers])
    print(header)
    ip = header.get("x-real-ip", ip.value[0])
    try:
        _ipinfo = await ipinfo.get_ip(ip.encode())
    except ValueError:
        _ipinfo = Ip_result()
    return json(Get_ua_result(ip,header,_ipinfo.data))


@docs(QQ_API_docs)
async def get_qq(qqnum:int,Qqinfo: _qq) -> Response:
    if qqnum < 10000 or qqnum > 9999999999:
        return not_found('qq号码错误')
    return json(await Qqinfo.Get_qqinfo(qqnum))

@docs(randimg_API_docs)
async def randImg(request: Request,rdimg:rdimg,method:str = 'pc',encode:str = None,number: int = 1) -> Response:
    ua = request.get_single_header(b'user-agent')
    if encode not in ['json',None]:
        encode = None
    if encode:
        return json({'code': 200,'url':rdimg.process(ua,encode,number,method)})
    return Response(302, [(b"Location", rdimg.process(ua,encode,number,method))])


@docs(yiyan_API_docs)
async def yiyan(request: Request,yy:Hitokoto,c:str = None,encode: str = None) -> Response:

    try:
        assert c is not None
        t = request.query.get('c')
        slist = [x for x in t if x in yy.type_list]
        assert slist is not []
        result = yy.cut_get_yiyan(slist)
    except Exception:
        result = yy.get_yiyan()
    return html(str(result)) if encode == 'text' else pretty_json(result)

if Config['qq']['enable']:
    add_get("/qq/{qqnum}",get_qq)
if Config['ip']['enable']:
    add_get("/ip/{str:ip}",get_ip)
if Config['yiyan']['enable']:
    add_get("/yiyan",yiyan)
if Config['randimg']['enable']:
    add_get('/randimg',randImg)
if Config['ua']['enable']:
    add_get('/ua',get_ua)