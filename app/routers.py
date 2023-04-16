import orjson
from blacksheep import Content, FromQuery
from blacksheep.messages import Request, Response
from blacksheep.server.bindings import ServerInfo, FromServices, FromHeader, FromRoute
from blacksheep.server.routing import Router
from blacksheep.server.responses import redirect, bad_request
from modules.ip_todo import IpUtils
from modules.qq_todo import QQUtils
from modules.yiyan_todo import Hitokoto
from modules.rand.randimg import Randimg as rdimg
from dataclass import UADataClass, IpResult
from app.docs import (
    UA_API_docs,
    ip_API_docs,
    docs,
    randimg_API_docs,
    yiyan_API_docs,
    QQ_API_docs,
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


@docs(ip_API_docs)
@get("/ip/{ip}")
async def get_ip(ipinfo: FromServices[IpUtils], ip: FromQuery[bytes]) -> Response:
    try:
        return json(await ipinfo.value.get_ip(ip.value))
    except Exception as e:
        return Response(
            status=500,
            content=Content(
                b"application/json", orjson.dumps({"status": 500, "error": f"{e}"})
            ),
        )


@docs(UA_API_docs)
@get("/ua")
async def get_ua(
    request: Request,
    ip: ServerInfo,
    ipinfo: FromServices[IpUtils],
) -> Response:
    header = {i.decode(): j.decode() for i, j in request.headers}
    ip = header.get("x-real-ip", ip.value[0])
    try:
        _ipinfo = await ipinfo.value.get_ip(ip.encode())
    except ValueError:
        _ipinfo = IpResult()
    return json(UADataClass(ip, header, _ipinfo.data))


@docs(QQ_API_docs)
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


@docs(randimg_API_docs)
@get("/randimg")
async def rand_img(
    # request: Request,
    ua: FromUserAgent,
    rdimg: FromServices[rdimg],
    method: FromQuery[str] = FromQuery("pc"),
    encode: FromQuery[str] = FromQuery(None),
    number: FromQuery[int] = FromQuery(1),
) -> Response:
    # ua = request.get_single_header(b"user-agent")
    if encode.value not in ["json", None]:
        encode.value = None
    if encode.value:
        return json(
            {
                "code": 200,
                "url": rdimg.value.process(ua.value, number.value, method.value).split(
                    " "
                ),
            }
        )
    return Response(
        302,
        [
            (
                b"Location",
                rdimg.value.process(ua.value, number.value, method.value).encode(),
            )
        ],
    )


@docs(yiyan_API_docs)
@get("/yiyan")
async def yiyan(
    hitokoto: FromServices[Hitokoto], c: FromQuery[set] = FromQuery(set())
) -> Response:
    t = list(hitokoto.value.type_set & c.value)
    result = hitokoto.value.get_hitokoto(t)
    return pretty_json(result)
