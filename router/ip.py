from fastapi import APIRouter,Request
from modules.ip import ipp
router = APIRouter()
get_ip = ipp()
@router.get('')
async def get_ip_info(ip: str = None):
    info = get_ip.get_ipinfo(ip=ip)
    return {"ip":ip,"data":info['data'],"code":info['code']}