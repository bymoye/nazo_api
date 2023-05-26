# 食用说明

使用本 API 请具有一定基础

本程序基于 [BlackSheep](https://github.com/Neoteroi/BlackSheep) 搭建

开发环境为 `Python 3.11`

请先将应用目录`(nazo_api)`的 `.env.example` 重命名为 `.env` 并修改其中的配置

本程序需要 GeoIP 库(本库不提供下载)

请自行到 [Maxmind](https://www.maxmind.com/en/accounts/) 下载 `GeoLite2-City.mmdb` 并放到 `nazo_api/src` 目录中

本程序需要 ip2asn 库(本库不提供下载)

请自行到 [iptoasn](https://iptoasn.com/) 下载 `ip2asn-v4.tsv`和`ip2asn-v6.tsv` 并放到 `src` 目录中

使用 `Dockerfile` 进行安装使用

`./build.sh` 中为构建指令

`./start.sh` 中为运行指令

图片请使用 [nazo_image_utils](https://github.com/bymoye/nazo_image_utils) 生成

一言库使用 [sentences-bundle](https://github.com/hitokoto-osc/sentences-bundle)

## 废案~~建议~~

虽然可以直接使用 `uvicorn`，但是还是建议使用 [nginx-unit](https://unit.nginx.org/installation/)

因为`nginx-unit`的性能高 如使用`nginx-unit`的话可以使用 `unit.config` 作为配置文件

需要修改`path`和`working_directory`

个人使用 unit 编译:

```
git clone https://github.com/nginx/unit
cd unit
./configure --prefix=/usr/local/unit --group=unit --user=unit --openssl --no-ipv6 --control=unix:/var/run/control.unit.sock
make && make install
```

编译 unit-python3.10:

```
./configure python --module=py310 --config=python3.10-config
make && make install
```

# 已实现功能

- QQ 昵称/头像获取
- 一言
- IP 定位
- UA
- 随机图

# 待做

- [x] 为 client 做限制防止并发时带来的崩溃

* bilibili_API
* 重写 ip2asn

# 更新日志

- 2023-05-14 迁移 model 中的大量代码到单独的模块

  1. [nazo_image_utils](https://github.com/bymoye/nazo_image_utils) 主图片处理 / 随机图 url 生成
  2. [nazo_rand](https://github.com/bymoye/nazo_rand) 随机数生成
  3. [nazo_ip2asn](https://github.com/bymoye/nazo_ip2asn) ip2asn 的文件处理/查找实现
  4. [webp_support](https://github.com/bymoye/webp_support) webp 支持检查

- 2023-04-24 重构大量代码
  1. 使用 ua 检查是否支持 webp 拆分为一个单独的模块: [webp_support](https://github.com/bymoye/webp_support)
  2. 使随机数拆分为一个单独的模块: [nazo_rand](https://github.com/bymoye/nazo_rand)
  3. 使随机图在使用 c 特性实现.
  4. 使 ip2asn 使用 c++17 特性.
- 2022-12-18 废案: C++实现 yiyan 随机 (提升不大)
- 2022-03-22 重写随机图模块
- 2021-10-28 完善 Config
- 2021-10-24 修正 QQAPI 接口编码问题

  > 做了一个有趣的实验, 将`sqlite3`替换为 `aiosqlite`.
  > 可是替换完成之后发现一个问题.
  > 那就是`aiosqlite`的性能反而没有`sqlite3`的性能高.
  > 原因不明 所以做了回滚. 目前还是使用`sqlite3`

- 2021-11-03 完善 docs
- 2021-10-22 避免多余的开销
- 2021-10-21 完善 docs
- 2021-10-20 完成程序的重构 放弃 FastApi ,拥抱 BlackSheep
