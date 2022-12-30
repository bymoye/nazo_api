from blacksheep import Content
from blacksheep.messages import Request, Response
from blacksheep.server.bindings import ServerInfo
from blacksheep.server.routing import Router
from blacksheep.server.responses import redirect, bad_request
import orjson
from modules.ip_todo import IpUtils
from modules.qq_todo import QQUtils
from modules.yiyan_todo import Hitokoto
from modules.rand.randimg import Randimg as rdimg
from dataclass import UADataClass, IpResult, config
from app.docs import (
    UA_API_docs,
    ip_API_docs,
    docs,
    randimg_API_docs,
    yiyan_API_docs,
    QQ_API_docs,
)
from app.jsonres import json, pretty_json
from app.services import service
from config import Module

router = Router()
get = router.get
add_get = router.add_get
g_config: Module = service.build_provider().get(config).config.module

# 未定义路由
def fallback() -> Response:
    return json(status=404, data={"msg": "这里不是你该来的地方"})


router.fallback = fallback


@docs.ignore()
@get("/")
async def index():
    return redirect("/docs")


@docs(ip_API_docs)
async def get_ip(ipinfo: IpUtils, ip: bytes) -> Response:
    print(ip)
    try:
        return json(await ipinfo.get_ip(ip))
    except Exception as e:
        return Response(
            status=500,
            content=Content(
                b"application/json", orjson.dumps({"status": 500, "error": f"{e}"})
            ),
        )


@docs(UA_API_docs)
async def get_ua(request: Request, ip: ServerInfo, ipinfo: IpUtils) -> Response:
    header = dict([(i.decode(), j.decode()) for i, j in request.headers])
    print(header)
    ip = header.get("x-real-ip", ip.value[0])
    try:
        _ipinfo = await ipinfo.get_ip(ip.encode())
    except ValueError:
        _ipinfo = IpResult()
    return json(UADataClass(ip, header, _ipinfo.data))


@docs(QQ_API_docs)
async def get_qq(qqnum: str, qq_utils: QQUtils) -> Response:
    if (
        (not qqnum.isdigit())
        or (qqnum.startswith("0"))
        or (len(qqnum) > 11)
        or (len(qqnum) < 5)
    ):
        return bad_request("qq号码错误")
    status, result = await qq_utils.get_qqinfo(qqnum)
    return json(result) if status else bad_request(result)


@docs(randimg_API_docs)
async def rand_img(
    request: Request,
    rdimg: rdimg,
    method: str = "pc",
    encode: str = None,
    number: int = 1,
) -> Response:
    ua = request.get_single_header(b"user-agent")
    if encode not in ["json", None]:
        encode = None
    if encode:
        return json({"code": 200, "url": rdimg.process(ua, encode, number, method)})
    return Response(302, [(b"Location", rdimg.process(ua, encode, number, method))])


@docs(yiyan_API_docs)
async def yiyan(request: Request, hitokoto: Hitokoto) -> Response:
    t = request.query.get("c", [])
    if t:
        t = list(set(hitokoto.type_list) & set(t))
    result = hitokoto.get_hitokoto(t)
    return pretty_json(result)


if g_config.qq.enable:
    add_get("/qq/{str:qqnum}", get_qq)
if g_config.ip.enable:
    add_get("/ip/{str:ip}", get_ip)
if g_config.yiyan.enable:
    add_get("/yiyan", yiyan)
if g_config.randimg.enable:
    add_get("/randimg", rand_img)
if g_config.ua.enable:
    add_get("/ua", get_ua)
