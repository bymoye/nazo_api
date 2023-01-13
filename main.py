from blacksheep import Content, Request, Response
from blacksheep.server import Application
from modules.rand import randimg
from modules import ip_todo, sql_todo, qq_todo, yiyan_todo
from app import docs, service, router
from dataclass import sql, config
import orjson
from blacksheep.plugins import json
from config import _ApiConfig

Config: _ApiConfig = service.build_provider().get(config).config
# 初始化
app = Application(router=router, services=service)
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
json.use(loads=orjson.loads, dumps=serialize, pretty_dumps=pretty_json_dumps)
# 发生错误时返回
def handler_error(request: Request, exc: Exception) -> Response:
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
    app.services.add_instance(sql_todo.SelfSqlite(), declared_class=sql)
    provider = app.services.build_provider()
    app.services.add_instance(qq_todo.QQUtils(provider.get(sql)))
    app.services.add_instance(ip_todo.IpUtils())
    app.services.add_instance(yiyan_todo.Hitokoto())
    app.services.add_instance(randimg.Randimg())


# 生命周期：启动后
@app.after_start
async def after_start(app: Application) -> None:
    provider = app.services.build_provider()
    yiyan: yiyan_todo.Hitokoto = provider.get("Hitokoto")
    await yiyan.init()


# 生命周期：停止时
@app.on_stop
async def on_stop(app: Application) -> None:
    await app.service_provider[sql].close()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app=app, port=Config.god.port, limit_concurrency=500)
