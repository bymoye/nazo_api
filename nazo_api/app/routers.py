from blacksheep import FromQuery
from blacksheep.messages import Request, Response
from blacksheep.server.bindings import ServerInfo, FromServices, FromHeader, FromRoute
from blacksheep.server.routing import Router
from blacksheep.server.responses import redirect, bad_request
from modules.ip_todo import IpUtils
from modules.yiyan_todo import Hitokoto
from nazo_image_utils import RandImage
from dataclass import UADataClass, IpResult
from app.docs import (
    ua_docs,
    ip_docs,
    docs,
    randimg_docs,
    yiyan_docs,
)
from app.jsonres import json, pretty_json
from time import time_ns

router = Router()
get = router.get


# 未定义路由
def fallback() -> Response:
    return json(status=404, data={"msg": "这里不是你该来的地方"})


router.fallback = fallback


@docs.ignore()
@get("/")
async def index():
    return redirect("/docs")


@docs(ip_docs)
@get("/ip/{ip}")
async def get_ip(ipinfo: FromServices[IpUtils], ip: FromRoute[bytes]) -> Response:
    try:
        return json(ipinfo.value.get_ip(ip.value))
    except Exception as e:
        return json({"status": 500, "error": f"{e}"}, status=500)


@docs(ua_docs)
@get("/ua")
async def get_ua(
    request: Request,
    ip: ServerInfo,
    ipinfo: FromServices[IpUtils],
) -> Response:
    header = {i.decode(): j.decode() for i, j in request.headers}
    # request.get_first_header(b"x-real-ip")
    # _ip = header.get("x-real-ip", ip.value[0])
    _ip = header.get("x-user-ip", header.get("x-real-ip", ip.value[0]))
    try:
        _ipinfo = ipinfo.value.get_ip(_ip.encode())
    except ValueError:
        _ipinfo = IpResult()
    return json(UADataClass(_ip, header, _ipinfo.data))


class FromUserAgent(FromHeader[bytes]):
    name = "user-agent"


@docs(randimg_docs)
@get("/randimg")
async def rand_img(
    # request: Request,
    ua: FromUserAgent,
    rdimg: FromServices[RandImage],
    platform: FromQuery[bytes] = FromQuery(b"pc"),
    encode: FromQuery[bytes] = FromQuery(b"redirect"),
    number: FromQuery[int] = FromQuery(1),
) -> Response:
    # ua = request.get_single_header(b"user-agent")
    if encode.value not in {b"json", b"redirect"}:
        return bad_request("encode参数错误")
    urls = rdimg.value.process(ua.value, number.value, platform.value, encode.value)
    if isinstance(urls, list):
        return json(
            {
                "code": 200,
                "url": urls,
            }
        )
    return Response(
        status=302,
        headers=[
            (
                b"Location",
                urls,
            )
        ],
    )


@docs(yiyan_docs)
@get("/yiyan")
async def yiyan(
    hitokoto: FromServices[Hitokoto], c: FromQuery[set] = FromQuery(set())
) -> Response:
    t = list(hitokoto.value.type_set & c.value)
    result = hitokoto.value.get_hitokoto(t)
    return pretty_json(result)


@get("/timestamp")
async def timestamp() -> Response:
    return Response(
        status=204,
        headers=[
            (
                b"timestamp",
                f"{time_ns() // 1000000}".encode(),
            )
        ],
    )
