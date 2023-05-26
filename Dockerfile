FROM unit:1.30.0-python3.11

COPY ./nazo_api/requirements.txt /config/requirements.txt

# 更改apt为阿里云源
RUN sed -i 's/archive.ubuntu.com/mirrors.aliyun.com/g' /etc/apt/sources.list

# 安装libmaxminddb和libmaxminddb-dev
RUN apt-get update && apt-get install -y libmaxminddb0 libmaxminddb-dev mmdb-bin

# 清理apt缓存
RUN apt-get clean && rm -rf /var/lib/apt/lists/*

RUN python3 -m pip config set global.index-url https://mirrors.aliyun.com/pypi/simple/

RUN python3 -m pip install -r /config/requirements.txt
