from fastapi import APIRouter,Request
import geoip2.database
router = APIRouter()
reader = geoip2.database.Reader('.\GeoLite2-city.mmdb')
readerasn = geoip2.database.Reader('.\GeoLite2-ASN.mmdb')


# print("地区：{}({})".format(response.continent.names["es"],
#                                        response.continent.names["zh-CN"]))

# print("国家：{}({}) ，简称:{}".format(response.country.name,
#                                                         response.country.names["zh-CN"],
#                                                         response.country.iso_code))

# print("洲／省：{}({})".format(response.subdivisions.most_specific.name,
#                                           response.subdivisions.most_specific.names["zh-CN"]))

# print("城市：{}({})".format(response.city.name, 
#                                           response.city.names["zh-CN"]))

# print("经度：{}，纬度{}".format(response.location.longitude,
#                                             response.location.latitude))

# print("时区：{}".format(response.location.time_zone))

# print("邮编:{}".format(response.postal.code))

# print("IP:{}".format(responseasn.ip_address))
# print("IP:{}".format(response))
@router.get("/")
def read_root(request: Request):
    header = request.headers
    if 'x-forward-for' in header:
        ip = header['x-forward-for']
    else:
        ip = request.client.host
    response = reader.city(ip)
    return {"header": header,"ip":ip,"all":str(request),"info":}