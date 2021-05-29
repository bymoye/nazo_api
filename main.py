import grequests
import ujson
from fastapi import FastAPI, status, Path, Query
from fastapi.responses import ORJSONResponse
from fastapi.exceptions import StarletteHTTPException
from router.qq import router as qqrouter
from router.yiyan import router as yyrouter
from router.ip import router as iprouter
# 读取config配置
def getConfig(json_file='config.json'):
    with open(json_file,"r",encoding='utf8') as file:
        return ujson.load(file)
# 全局配置
config = getConfig(json_file='config.json')
# 初始化FastAPI
app = FastAPI(title="nmx API",
              description="基于FastAPI搭建",
              version="0.1.0",
              
            )

# QQ信息
app.include_router(
    qqrouter,
    prefix = config['prefix'] + config['qq']['prefix'],
    tags=['qq']
)
# 一言
app.include_router(
    yyrouter,
    tags=['yiyan'],
    prefix = config['prefix'] + config['yiyan']['prefix']
)

app.include_router(
    iprouter,
    tags=['ip'],
    prefix = config['prefix'] + config['ip']['prefix']
)

# 定义默认
@app.exception_handler(StarletteHTTPException)
async def not_found(request, exc):
    return ORJSONResponse({"code": 400, "message": "这里不是你应该来的地方."},status_code=status.HTTP_404_NOT_FOUND)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app=app, limit_concurrency=500)
