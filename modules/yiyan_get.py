import grequests
import orjson,ujson
import requests
import os
class yiyan:
    type_cont = {}
    type_list = {}
    # 获取hitokoto
    def get_yiyan(self):
        req_list = requests.get("https://cdn.jsdelivr.net/gh/hitokoto-osc/sentences-bundle/categories.json").text
        a = [item['key'] for item in orjson.loads(req_list)]
        hitokoto_begin = 'https://cdn.jsdelivr.net/gh/hitokoto-osc/sentences-bundle/sentences/'
        urls = [grequests.get(hitokoto_begin + item + '.json') for item in a]
        list = grequests.map(urls)
        [open('./sentences/'+a[count]+'.json', mode='wb').write(list[count].content) for count in range(len(urls))]
        open('./sentences/all.json', mode='wb').write(orjson.dumps(a))
    # 转为json
    def to_json(self):
        with open("./sentences/all.json","r",encoding='utf8') as file:
            self.type_list = ujson.load(file)
        for i in self.type_list:
            with open("./sentences/" + i + '.json',"r",encoding='utf8') as file:
                self.type_cont[i] = ujson.load(file)
    # 初始化
    def __init__(self):
        if not os.path.exists(r'./sentences'):
            os.makedirs(r'./sentences')
        if not os.path.exists(r'./sentences/all.json'):
            self.get_yiyan()   
        self.to_json()