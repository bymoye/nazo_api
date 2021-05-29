from fastapi import APIRouter,Request

router = APIRouter()


@router.get("/")
def read_root(request: Request):
    header = request.headers
    if 'x-forward-for' in header:
        ip = header['x-forward-for']
    else:
        ip = request.client.host
    return {"header": header,"ip":ip}