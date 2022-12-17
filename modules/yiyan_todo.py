from blacksheep.client import ClientSession
import os,orjson,fastrand
class _yiyan:
    def __init__(self,client:ClientSession):
        self.type_cont,self.type_cont_len = {},{}
        self.client = client

    async def init(self):
        print('初始化一言')
        if not os.path.exists(r'./sentences'):
            os.makedirs(r'./sentences')
        if not os.path.exists(r'./sentences/all.json'):
            await self.download_yiyan()
        self.load()
        
    async def download_yiyan(self) -> None:
        print('从jsdelivr下载一言库')
        hitokoto_list = await self.client.get("https://cdn.jsdelivr.net/gh/hitokoto-osc/sentences-bundle@latest/categories.json")
        assert (hitokoto_list is not None),'请求错误'
        tm = await hitokoto_list.json()
        hitokoto_begin = 'https://cdn.jsdelivr.net/gh/hitokoto-osc/sentences-bundle/sentences/'
        hitokoto = [await j.json() for j in [await self.client.get(hitokoto_begin + i['key'] + '.json') for i in tm]]
        for n in range(len(tm)):
            with open("./sentences/" + tm[n]['key'] + '.json', mode='wb') as f:
                f.write(orjson.dumps(hitokoto[n]))
        with open('./sentences/all.json', mode='wb') as f:
            f.write(orjson.dumps(tm))
        print('下载完成')
        
    def load(self) -> None:
        print('加载一言')
        with open("./sentences/all.json","r",encoding='utf8') as file:
            self.type_list = [i['key'] for i in orjson.loads(file.read())]
            self.type_list_len = len(self.type_list)
        for i in self.type_list:
            with open(f"./sentences/{i}.json","r",encoding='utf8') as file:
                self.type_cont[i] = orjson.loads(file.read)
                self.type_cont_len[i] = len(self.type_cont[i])
        print('加载完毕')
        
    def get_yiyan(self) -> dict:
        n = self.type_list[fastrand.pcg32bounded(self.type_list_len)]
        return self.type_cont[n][fastrand.pcg32bounded(self.type_cont_len[n])]
    
    def cut_get_yiyan(self,l:list) -> dict:
        _len = len(l)
        if _len != 1:
            n = self.type_list[fastrand.pcg32bounded(_len)]
            return self.type_cont[n][fastrand.pcg32bounded(self.type_cont_len[n])]
        return self.type_cont[l[0]][fastrand.pcg32bounded(self.type_cont_len[l[0]])]