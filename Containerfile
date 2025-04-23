FROM unit:1.34.1-python3.13

COPY ./nazo_api/requirements.txt /config/requirements.txt

RUN sed -i "s@http://deb.debian.org/debian@http://mirrors.tencent.com/debian@g" /etc/apt/sources.list.d/debian.sources

# 安装libmaxminddb和libmaxminddb-dev
RUN apt-get update && apt-get install -y libmaxminddb0 libmaxminddb-dev mmdb-bin

# 清理apt缓存
RUN apt-get clean && rm -rf /var/lib/apt/lists/*

RUN python3 -m pip config set global.index-url https://mirrors.tencent.com/pypi/simple

RUN python3 -m pip install -r /config/requirements.txt
