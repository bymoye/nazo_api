from os import stat
from fastapi import APIRouter,Request,status
from fastapi.responses import ORJSONResponse,RedirectResponse
import random,re

router = APIRouter()
imgurl_pc = []
imgurl_mb = []
with open("./src/img_url_pc.txt") as f:
    imgurl_pc = ''.join(f.readlines()).strip('\n').splitlines()
with open("./src/img_url_mb.txt") as f:
    imgurl_mb = ''.join(f.readlines()).strip('\n').splitlines()
version_list = {'Firefox':65,
                'Chrome':32,
                'Edg':18,
                'Version':14,
                'Opera':19,
            }

@router.get('')
async def randomimg(request: Request,encode:str = None,n: int = 1,type:str = 'pc'):
    ua = request.headers.get('user-agent')
    if ua == None or (encode not in ['json',None]) or (type not in ['pc','mobile']):
        return ORJSONResponse(status_code=status.HTTP_400_BAD_REQUEST,content={"code":400,"msg":"非法访问"})
    if n > 10:
        return ORJSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"code":400,"msg":"数量超过允许上限"})
    
    if 'Chrome' in ua:
        reg = "(Chrome)\/(\d+)"
    else:
        reg = "(Firefox|Chrome|Version|Opera|Edg)\/(\d+)"
    match = re.search(reg,ua)
    if match == None or version_list.get(match.group(1)) > int(match.group(2)):
        _format = "!q80.jpeg"
    else:
        _format = "!q80.webp"

    if encode == None:
        return RedirectResponse(random.choice(imgurl_pc) + _format)
    if encode == 'json':
        if type == 'mobile':
            url = random.sample(imgurl_mb,n)
        else:
            url = random.sample(imgurl_pc,n)
        url = ["".join([i,_format]) for i in url]
        return ORJSONResponse(status_code=status.HTTP_200_OK,content={"code":200,"url":url})