from fastapi import APIRouter,status, Path, Query
from fastapi.responses import ORJSONResponse
from typing import List, Optional
import random
from modules.yiyan_get import yiyan

router = APIRouter()
yy = yiyan()
@router.get("")
async def yiy(t: Optional[List[str]] = Query(None), encode: str = None):
    # 判断是否有带参数
    if (t != None):
        slist = [x for x in t if x in yy.type_list]
        sel_type = random.choice(slist)
    else:
        sel_type = random.choice(yy.type_list)
    # 判断是否带encode参数
    if encode == 'text':
        headers = {
            'content-type': 'text/html; charset=utf-8'
        }
    else:
        headers = {
            'content-type': 'application/json; charset=utf-8'
        }
    return ORJSONResponse(status_code=status.HTTP_200_OK, content=random.choice(yy.type_cont[sel_type]), headers=headers)