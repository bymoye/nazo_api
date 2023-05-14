import os
from dotenv import load_dotenv
import orjson
from blacksheep import Content, Request, Response, Application

# from modules.rand import randimg
from nazo_image_utils import RandImage
from modules import IpUtils, SelfSqlite, QQUtils, Hitokoto
from app import docs, router
from blacksheep.plugins import json

load_dotenv()
# 初始化
app = Application(router=router)
# redoc文档
docs.bind_app(app)
# CORS跨域问题
app.use_cors(
    allow_methods="*",
    allow_origins="*",
    allow_headers="*",
    max_age=2592000,
)


# 使用orjson
def serialize(value) -> str:
    return orjson.dumps(value).decode("utf8")


# 使用orjson格式化输出
def pretty_json_dumps(obj):
    return orjson.dumps(obj, option=orjson.OPT_INDENT_2).decode("utf8")


# 使Blacksheep绑定
json.use(loads=orjson.loads, dumps=serialize, pretty_dumps=pretty_json_dumps)  # type: ignore


# 发生错误时返回
async def handler_error(request: Request, exc: Exception) -> Response:
    return Response(
        status=500,
        content=Content(
            b"application/json", orjson.dumps({"status": 500, "error": f"{exc}"})
        ),
    )


app.handle_internal_server_error = handler_error


# 生命周期：启动前
@app.on_start
async def before_start(app: Application) -> None:
    app.services.add_instance(SelfSqlite())
    app.services.add_instance(QQUtils(app.services.build_provider().get(SelfSqlite)))
    app.services.add_instance(
        IpUtils(
            os.getenv("GEOLITE2_CITY_PATH", "./src/GeoLite2-City.mmdb"),
            os.getenv("IP2ASN_V4_PATH", "./src/ip2asn-v4.tsv"),
            os.getenv("IP2ASN_V6_PATH", "./src/ip2asn-v6.tsv"),
        )
    )
    app.services.add_instance(Hitokoto())
    app.services.add_instance(
        RandImage(
            os.getenv("MANIFEST_PATH", "./src/manifest.json"),
            os.getenv("MANIFEST_MOBILE_PATH", "./src/manifest_mobile.json"),
            os.getenv("IMAGE_DOMAIN", "https://example.com"),
        )
    )


# 生命周期：启动后
@app.after_start
async def after_start(app: Application) -> None:
    provider = app.services.build_provider()
    yiyan: Hitokoto = provider.get("Hitokoto")
    await yiyan.init()


# 生命周期：停止时
@app.on_stop
async def on_stop(app: Application) -> None:
    await app.service_provider[SelfSqlite].close()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app=app, port=os.environ.get("port", 5000), limit_concurrency=500)  # type: ignore
