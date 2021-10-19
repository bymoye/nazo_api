import orjson,ujson,yaml
import grequests
from fastapi import FastAPI, status, Path, Query
from fastapi.responses import ORJSONResponse
from fastapi.exceptions import StarletteHTTPException
from fastapi.middleware.cors import CORSMiddleware
from router.qq import router as qqrouter
from router.yiyan import router as yyrouter
from router.ip import router as iprouter
from router.random_img import router as imgrouter
from router.UA import router as UArouter
# 读取config配置
def getConfig(yaml_file='config.yaml'):
    file = open(yaml_file, 'r', encoding="utf-8")
    file_data = file.read()
    file.close()
    config = yaml.load(file_data, Loader=yaml.FullLoader)
    return dict(config)

# 全局配置
config = getConfig(yaml_file='config.yaml')
# 初始化FastAPI
app = FastAPI(title="nmx API",
              description="基于FastAPI搭建",
              version="0.1.0",
            )
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# QQ信息
app.include_router(
    qqrouter,
    prefix = config['global']['prefix'] + config['module']['qq']['prefix'],
    tags = ['qq']
)
# 一言
app.include_router(
    yyrouter,
    tags = ['yiyan'],
    prefix = config['global']['prefix'] + config['module']['yiyan']['prefix']
)
# ip
app.include_router(
    iprouter,
    tags = ['ip'],
    prefix = config['global']['prefix'] + config['module']['ip']['prefix']
)
# 随机图
app.include_router(
    imgrouter,
    tags = ['randomimg'],
    prefix = config['global']['prefix'] + config['module']['randomimg']['prefix']
)
# UA
app.include_router(
    UArouter,
    tags=['UA'],
    prefix = config['global']['prefix'] + config['module']['UA']['prefix']
)

# 定义默认
@app.exception_handler(StarletteHTTPException)
async def not_found(request, exc):
    return ORJSONResponse({"code": 400, "message": "这里不是你应该来的地方."},status_code=status.HTTP_400_BAD_REQUEST)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app=app, limit_concurrency=500)
