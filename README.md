# 食用说明

使用本API请具有一定基础

本程序基于 [BlackSheep](https://github.com/Neoteroi/BlackSheep) 搭建

开发环境为 `Python 3.10`

因为用到 `orjson` 所以需要安装 `rust` 以完成 `orjson` 的安装

因为基于 `BlackSheep` 所以需要 `Cython` 所以需要 `gcc`

(环境方面不再描述 环境问题按照提示处理)

本程序需要 GeoIP 库(本库不提供下载)

请自行到 [Maxmind](https://www.maxmind.com/en/accounts/216453/geoip/downloads) 下载 `GeoLite2-City.mmdb` 并放到 `src` 目录中

本程序需要 ip2asn 库(本库不提供下载)

请自行到 [iptoasn](https://iptoasn.com/) 下载 `ip2asn-v4-u32.tsv`和`ip2asn-v6.tsv` 并放到 `src` 目录中

请修改 `.env.example` 更名为 `.env` 并修改内的键值

IP接口备选方案使用 [高德开放平台](https://console.amap.com/dev/key/app) 请 创建一个 Key 再将这个KEY放到 .env中的 ip_key 值

随机图库放在 `./src/img_url_mb.txt` 和 `./src/img_url_pc.txt` 中 可以自行修改其中的链接 

这里我是用的是[fghrsh](https://img.fghrsh.net) 大佬的图床 所以有处理规则

可以自行修改 `./app/routers.py` 中的 `async def Randimg`

一言库使用 [sentences-bundle](https://github.com/hitokoto-osc/sentences-bundle)


# 更新日志
2021-10-20 完成程序的重构 放弃 FastApi ,拥抱 BlackSheep