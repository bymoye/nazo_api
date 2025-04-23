import msgspec
from typing import Optional
from nazo_rand import randbelow
from blacksheep.client import ClientSession
from logging import getLogger
from pathlib import Path

logger = getLogger(__name__)


class Hitokoto:
    def __init__(self):
        self.type_cont, self.type_cont_len = {}, {}
        self.base_url = (
            "https://fastly.jsdelivr.net/gh/hitokoto-osc/sentences-bundle@latest/"
        )
        self.sentences_path = Path("./sentences")

    async def init(self):
        # print("初始化一言")
        logger.info("初始化一言")
        if not self.sentences_path.exists():
            Path("./sentences").mkdir(parents=True, exist_ok=True)
        if not self.sentences_path.joinpath("all.json").exists():
            await self.download_yiyan()
        self.load()

    async def download_yiyan(self) -> None:
        # print("从jsdelivr下载一言库")
        logger.info("从jsdelivr下载一言库")
        async with ClientSession() as client:

            r = await client.get(f"{self.base_url}categories.json")
            assert r.status == 200
            hitokoto_list = await r.json()
            hitokoto = [
                await j.json()
                for j in [
                    await client.get(f"{self.base_url}sentences/{i['key']}.json")
                    for i in hitokoto_list
                ]
            ]
        for n in range(len(hitokoto_list)):
            self.sentences_path.joinpath(f"{hitokoto_list[n]['key']}.json").write_bytes(
                msgspec.json.encode(hitokoto[n])
            )
        self.sentences_path.joinpath("all.json").write_bytes(
            msgspec.json.encode(hitokoto_list)
        )
        # print("下载完成")
        logger.info("下载完成")

    def load(self) -> None:
        # print("加载一言")
        logger.info("加载一言")

        self.type_list = [
            i["key"]
            for i in msgspec.json.decode(
                self.sentences_path.joinpath("all.json").read_bytes()
            )
        ]
        self.type_set = set(self.type_list)
        self.type_list_len = len(self.type_list)
        for i in self.type_list:
            self.type_cont[i] = msgspec.json.decode(
                self.sentences_path.joinpath(f"{i}.json").read_bytes()
            )
            self.type_cont_len[i] = len(self.type_cont[i])
        # print("加载完毕")
        logger.info("加载完毕")

    def get_hitokoto(self, l: Optional[list] = None) -> dict:
        n = l[randbelow(len(l))] if l else self.type_list[randbelow(self.type_list_len)]
        return self.type_cont[n][randbelow(self.type_cont_len[n])]
