import os
import typing as t
from dotenv import load_dotenv

from msgspec import json
from rodi import Container
from blacksheep import Content, Request, Response, Application

# from modules.rand import randimg
from nazo_image_utils import RandImage
from modules import IpUtils, SelfSqlite, Hitokoto
from app import docs, router


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


# 发生错误时返回
async def handler_error(request: Request, exc: Exception) -> Response:
    return Response(
        status=500,
        content=Content(
            b"application/json", json.encode({"status": 500, "error": f"{exc}"})
        ),
    )


app.handle_internal_server_error = handler_error


# 生命周期：启动前
@app.on_start
async def before_start(app: Application) -> None:
    container = t.cast(Container, app.services)
    container.add_instance(instance=SelfSqlite(), declared_class=None)
    container.add_instance(
        instance=IpUtils(
            os.getenv("GEOLITE2_CITY_PATH", "./src/GeoLite2-City.mmdb"),
            os.getenv("IP2ASN_V4_PATH", "./src/ip2asn-v4.tsv"),
            os.getenv("IP2ASN_V6_PATH", "./src/ip2asn-v6.tsv"),
        )
    )
    container.add_instance(Hitokoto())
    container.add_instance(
        instance=RandImage(
            os.getenv("MANIFEST_PATH", "./src/manifest.json"),
            os.getenv("MANIFEST_MOBILE_PATH", "./src/manifest_mobile.json"),
            os.getenv("IMAGE_DOMAIN", "https://example.com"),
        )
    )


# 生命周期：启动后
@app.after_start
async def after_start(app: Application) -> None:
    container = t.cast(Container, app.services)
    yiyan: Hitokoto = container.provider.get(Hitokoto)
    await yiyan.init()


# 生命周期：停止时
@app.on_stop
async def on_stop(app: Application) -> None:
    container = t.cast(Container, app.services)
    container.provider.get(SelfSqlite).close()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app=app, port=os.environ.get("port", 5000), limit_concurrency=500)  # type: ignore
