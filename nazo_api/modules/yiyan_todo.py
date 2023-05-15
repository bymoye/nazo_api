import os, orjson, httpx
from typing import Optional
from nazo_rand import randbelow


class Hitokoto:
    def __init__(self):
        self.type_cont, self.type_cont_len = {}, {}

    async def init(self):
        print("初始化一言")
        if not os.path.exists(r"./sentences"):
            os.makedirs(r"./sentences")
        if not os.path.exists(r"./sentences/all.json"):
            await self.download_yiyan()
        self.load()

    async def download_yiyan(self) -> None:
        print("从jsdelivr下载一言库")
        async with httpx.AsyncClient(
            base_url="https://cdn.jsdelivr.net/gh/hitokoto-osc/sentences-bundle@latest/"
        ) as client:
            r = await client.get("categories.json")
            assert r.status_code == 200
            hitokoto_list = r.json()
            hitokoto = [
                j.json()
                for j in [
                    await client.get(f"sentences/{i['key']}.json")
                    for i in hitokoto_list
                ]
            ]
        for n in range(len(hitokoto_list)):
            with open(f"./sentences/{hitokoto_list[n]['key']}.json", mode="wb") as f:
                f.write(orjson.dumps(hitokoto[n]))
        with open("./sentences/all.json", mode="wb") as f:
            f.write(orjson.dumps(hitokoto_list))
        print("下载完成")

    def load(self) -> None:
        print("加载一言")
        with open("./sentences/all.json", "r", encoding="utf8") as file:
            self.type_list = [i["key"] for i in orjson.loads(file.read())]
            self.type_set = set(self.type_list)
            self.type_list_len = len(self.type_list)
        for i in self.type_list:
            with open(f"./sentences/{i}.json", "r", encoding="utf8") as file:
                self.type_cont[i] = orjson.loads(file.read())
                self.type_cont_len[i] = len(self.type_cont[i])
        print("加载完毕")

    def get_hitokoto(self, l: Optional[list] = None) -> dict:
        n = l[randbelow(len(l))] if l else self.type_list[randbelow(self.type_list_len)]
        return self.type_cont[n][randbelow(self.type_cont_len[n])]
