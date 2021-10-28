from blacksheep.client import ClientSession
from blacksheep.server import Application
from modules import ip_todo,sql_todo,qq_todo,randimg_todo,yiyan_todo
from app import docs,service,router
from dataclass import sql,httpclient,config
import orjson
from blacksheep.plugins import json
# 初始化
app = Application(router=router,services=service)

docs.bind_app(app)
app.use_cors(
    allow_methods="*",
    allow_origins="*",
    allow_headers="*",
    max_age=2592000,
)
def serialize(value) -> str:
    return orjson.dumps(value).decode("utf8")

def pretty_json_dumps(obj):
    return orjson.dumps(obj,option=orjson.OPT_INDENT_2).decode("utf8")

json.use(
    loads = orjson.loads,
    dumps = serialize,
    pretty_dumps=pretty_json_dumps
    )

@app.on_start
async def before_start(app: Application) -> None:
    http_client = ClientSession(follow_redirects=False)
    app.services.add_instance(http_client, declared_class=httpclient)
    app.services.add_instance(sql_todo.sqlite(), declared_class=sql)
    provider = app.services.build_provider()
    app.services.add_instance(qq_todo._qq(http_client,provider.get(sql)))
    app.services.add_instance(ip_todo._ip(http_client, '' ,provider.get(sql)))
    app.services.add_instance(yiyan_todo._yiyan(http_client))
    app.services.add_instance(randimg_todo.randimg())

@app.after_start
async def after_start(app: Application) -> None:
    provider = app.services.build_provider()
    yiyan = provider.get('_yiyan')
    await yiyan.init()


@app.on_stop
async def on_stop(app: Application) -> None:
    await app.service_provider[sql].close()
    await app.service_provider[httpclient].close()


if __name__ == '__main__':
    import uvicorn
    Config = app.services.build_provider().get(config).config._global
    uvicorn.run(app=app, port = Config['port'] ,limit_concurrency=500)