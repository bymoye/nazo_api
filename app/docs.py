from blacksheep.server.openapi.v3 import OpenAPIHandler
from openapidocs.v3 import Contact, Info, Parameter
from dataclass import Get_ua_result,Ip_result,Qq_info,randimg_result,Ip_info
from blacksheep.server.openapi.common import (
    ContentInfo,
    EndpointDocs,
    HeaderInfo,
    ParameterInfo,
    RequestBodyInfo,
    ResponseExample,
    ResponseInfo,
)
docs = OpenAPIHandler(info=Info(title="nmx API", version="0.2.0",contact=Contact('迷与谜&bymoye','https://nmxc.ltd','s3moye@gmail.com')))

ip_API_docs = EndpointDocs(
    summary="获取IP信息(定位)",
    description="""一个获取IP信息的API,支持IP4和IP6,主要为GEOIP,备用为高德API
                   请求示例： /ip/8.8.8.8
    """,
    responses={
        200: ResponseInfo(
            "获取成功",
            content=[
                ContentInfo(
                    Ip_result,
                    examples=[
                        ResponseExample(
                            Ip_result(
                                ip = '8.8.8.8',
                                data = Ip_info(country='美国',province='null',city='null',AS=15169,isp='GOOGLE - Google LLC'),
                                code = 0
                            )
                        )
                    ]
                )
            ]
        )
    }
)

UA_API_docs = EndpointDocs(
    summary="获取浏览器UA信息及当前IP信息",
    description="""一个获取UA信息及当前IP信息的API""",
    responses={
        200: ResponseInfo(
            "获取成功",
            content=[
                ContentInfo(
                    Get_ua_result,
                    examples=[
                        ResponseExample(
                            Get_ua_result(
                                ip = '8.8.8.8',
                                header = {
                                        "host": "127.0.0.1:8000",
                                        "connection": "keep-alive",
                                        "pragma": "no-cache",
                                        "cache-control": "no-cache",
                                        "sec-ch-ua": "\"Chromium\";v=\"94\", \"Google Chrome\";v=\"94\", \";Not A Brand\";v=\"99\"",
                                        "sec-ch-ua-mobile": "?0",
                                        "sec-ch-ua-platform": "\"Windows\"",
                                        "dnt": "1",
                                        "upgrade-insecure-requests": "1",
                                        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36",
                                        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                                        "sec-fetch-site": "none",
                                        "sec-fetch-mode": "navigate",
                                        "sec-fetch-user": "?1",
                                        "sec-fetch-dest": "document",
                                        "accept-encoding": "gzip, deflate, br",
                                        "accept-language": "zh-CN,zh;q=0.9,zh-TW;q=0.8,en;q=0.7",
                                    },
                                ipinfo = Ip_info(country='美国',province='null',city='null',AS=15169,isp='GOOGLE - Google LLC')
                            )
                        )
                    ]
                )
            ]
        )
    }
)


randimg_API_docs = EndpointDocs(
    summary="获取随机图",
    description="一个获取随机图的API",
    parameters={"encode":ParameterInfo('json或留空'),
                "n":ParameterInfo("需要获取的数量,仅在encode为json时有效,该值不得大于10"),
                "type":ParameterInfo("类型该项仅包含pc和mobile两个值")},
    responses={
        200: ResponseInfo(
            "获取成功",
            content=[
                ContentInfo(
                    randimg_result,
                    examples=[
                        ResponseExample(
                            randimg_result(200,["https://fp1.fghrsh.net/2020/01/14/85d51dc748307d61bcc097053e2dc528.jpg!q80.webp","https://fp1.fghrsh.net/2020/01/31/def2642c77337f4a6fa5469fb0bb3e35.jpg!q80.webp","https://fp1.fghrsh.net/2020/01/31/6173b6c9993f48872b818d57afdb9535.jpg!q80.webp"])
                        )
                    ]
                )
            ],
        )
    }
)

yiyan_API_docs = EndpointDocs(
    summary="获取一言",
    description="一个获取一言的API",
    parameters={"c":ParameterInfo('类型,可以多个值,例如c=a&c=b,默认为全随机,类型有哪些可以参考hitokoto官方.'),
                "encode":ParameterInfo("编码,仅限text和json,默认为json")},
    responses={
        200: ResponseInfo(
            "获取成功",
            content=[
                ContentInfo(
                    type=dict,
                    examples=[
                        ResponseExample(
                            {
                            "id": 12,
                            "uuid": "21876029-7f74-4d10-86d8-70c724248f5d",
                            "hitokoto": "人经历风浪是会变得更强，可是船不同，日积月累的只有伤痛。",
                            "type": "a",
                            "from": "海贼王",
                            "from_who": 'null',
                            "creator": "Jonse",
                            "creator_uid": 0,
                            "reviewer": 0,
                            "commit_from": "web",
                            "created_at": "1468605909",
                            "length": 28
                            }
                        )
                    ]
                )
            ],
        )
    }
)

QQ_API_docs = EndpointDocs(
    summary="获取QQ昵称&头像",
    description="一个获取QQ昵称&头像的API",
    parameters={"qqnum":ParameterInfo('5-10位QQ号')},
    responses={
        200: ResponseInfo(
            "获取成功",
            content=[
                ContentInfo(
                    type=Qq_info,
                    examples=[
                        ResponseExample(
                            Qq_info(12345,12345,'http://thirdqq.qlogo.cn/g?b=sdk&k=ffxWIb7R5Rzpia88aM9SNXg&s=640&t=1555323417')
                        )
                    ]
                )
            ],
        )
    }
)