import orjson
from blacksheep import Content, FromQuery
from blacksheep.messages import Request, Response
from blacksheep.server.bindings import ServerInfo, FromServices, FromHeader, FromRoute
from blacksheep.server.routing import Router
from blacksheep.server.responses import redirect, bad_request
from modules.ip_todo import IpUtils
from modules.qq_todo import QQUtils
from modules.yiyan_todo import Hitokoto
from nazo_image_utils import RandImage
from dataclass import UADataClass, IpResult
from app.docs import (
    ua_docs,
    ip_docs,
    docs,
    randimg_docs,
    yiyan_docs,
    qq_docs,
)
from app.jsonres import json, pretty_json

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
        return Response(
            status=500,
            content=Content(
                b"application/json", orjson.dumps({"status": 500, "error": f"{e}"})
            ),
        )


@docs(ua_docs)
@get("/ua")
async def get_ua(
    request: Request,
    ip: ServerInfo,
    ipinfo: FromServices[IpUtils],
) -> Response:
    header = {i.decode(): j.decode() for i, j in request.headers}
    request.get_first_header(b"x-real-ip")
    _ip = header.get("x-real-ip", ip.value[0])
    try:
        _ipinfo = ipinfo.value.get_ip(_ip.encode())
    except ValueError:
        _ipinfo = IpResult()
    return json(UADataClass(_ip, header, _ipinfo.data))


@docs(qq_docs)
@get("/qq/{str:qqnum}")
async def get_qq(qqnum: FromRoute[str], qq_utils: FromServices[QQUtils]) -> Response:
    if (
        (not qqnum.value.isdigit())
        or (qqnum.value.startswith("0"))
        or not (5 < len(qqnum.value) < 11)
    ):
        return bad_request("qq号码错误")
    status, result = await qq_utils.value.get_qqinfo(qqnum.value)
    return json(result) if status else bad_request(result)


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
        302,
        [
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
