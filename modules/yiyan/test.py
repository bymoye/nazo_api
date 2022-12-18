import yiyan
from blacksheep import Content, Request, Response
from blacksheep.server import Application

app = Application()


@app.route("/")
async def index(request: Request) -> Response:
    # 获取request中的type列表
    # request_type = request.query.get("type")
    # print(request_type)
    return Response(
        status=200, content=Content(b"application/json", yiyan.get_test([]))
    )


import uvicorn

uvicorn.run(app)
