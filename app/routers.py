from blacksheep.messages import Request, Response
from blacksheep.server.bindings import ServerInfo
from blacksheep.server.routing import Router
from blacksheep.server.responses import redirect, html, bad_request,not_found
from modules.ip_todo import _ip
from modules.qq_todo import _qq
from modules.yiyan_todo import _yiyan
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
async def Get_ip(ipinfo: _ip, ip: str) -> Response:
    try:
        return json(await ipinfo.GetIp(ip))
    except Exception as e:
        return bad_request(e.__str__())

@docs(UA_API_docs)
async def Get_ua(request: Request,ip:ServerInfo,ipinfo: _ip) -> Response:
    header = dict([(bytes.decode(i),bytes.decode(j)) for i,j in request.headers])
    ip = header['x-real-ip'] if "x-real-ip" in header.keys() else ip.value[0]
    _ipinfo = await ipinfo.GetIp(ip)
    return json(Get_ua_result(ip,header,_ipinfo.data))


@docs(QQ_API_docs)
async def Get_Qq(qqnum:int,Qqinfo: _qq) -> Response:
    if qqnum < 10000 or qqnum > 9999999999:
        return not_found('qq号码错误')
    return json(await Qqinfo.Get_qqinfo(qqnum))

@docs(randimg_API_docs)
async def Randimg(request: Request,rdimg:rdimg,encode:str = None,number: int = 1,method:str = 'pc') -> Response:
    ua = request.get_first_header(b'user-agent')
    # try:
    if encode not in ['json',None]:
        encode = None
    if encode:
        return json(randimg_result(200,rdimg.process(ua,encode,number,method)))
    return redirect(rdimg.process(ua,encode,number,method))


@docs(yiyan_API_docs)
async def yiyan(request: Request,yy:_yiyan,c:str = None,encode: str = None) -> Response:

    try:
        assert c is not None
        t = request.query.get('c')
        slist = [x for x in t if x in yy.type_list]
        assert slist is not []
        result = yy.cut_get_yiyan(slist)
    except:
        result = yy.get_yiyan()
    if encode == 'text':
        return html(str(result))
    else:
        return pretty_json(result)

if Config['qq']['enable']:
    add_get("/qq/{qqnum}",Get_Qq)
if Config['ip']['enable']:
    add_get("/ip/{str:ip}",Get_ip)
if Config['yiyan']['enable']:
    add_get("/yiyan",yiyan)
if Config['randimg']['enable']:
    add_get('/randimg',Randimg)
if Config['ua']['enable']:
    add_get('/ua',Get_ua)