FROM unit:1.30.0-python3.11

COPY ./nazo_api/requirements.txt /config/requirements.txt

RUN python3 -m pip config set global.index-url https://mirrors.aliyun.com/pypi/simple/

RUN python3 -m pip install -r /config/requirements.txt
