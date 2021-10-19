from fastapi import APIRouter,Request
from modules.ip import ipp
router = APIRouter()
get_ip = ipp()
@router.get('')
async def read_root(request: Request):
    client_host = request.headers
    ip = client_host['x-real-ip'] if "x-real-ip" in client_host.keys() else request.client.host
    ipinfo = get_ip.get_ipinfo(ip)
    return {"headers": client_host,"ip":ip}