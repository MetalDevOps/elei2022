import asyncio
from asyncio import futures
from utils.utils import MakeRequest
import json
import os
import aiohttp
import aiofiles
from pyunpack import Archive
from pathlib import Path


class ApiRequests(MakeRequest):
    def __init__(self):
        super().__init__()
        self.base_url = "https://resultados.tse.jus.br/oficial/ele2022"
        self.lista_siglas = [
            "ac",
            "al",
            "ap",
            "am",
            "ba",
            "ce",
            "df",
            "es",
            "zz",
            "go",
            "ma",
            "mt",
            "ms",
            "mg",
            "pr",
            "pb",
            "pa",
            "pe",
            "pi",
            "rj",
            "rn",
            "rs",
            "ro",
            "rr",
            "sc",
            "se",
            "sp",
            "to",
        ]
        # self.lista_siglas = ["zz"]

    def get(self, url, **kwargs):
        return self.request("GET", url, **kwargs)

    def get_mun_zon_sec(self):
        mun_zon_sec_dump = {}
        for i in self.lista_siglas:
            mun_zon_sec_dump[f"{i.casefold()}"] = []
            url = f"{self.base_url}/arquivo-urna/406/config/{i}/{i}-p000406-cs.json"
            response = self.get(url).json()["abr"]
            print(len(response[0]["mu"]))

            for j in range(len(response[0]["mu"])):
                mu = response[0]["mu"][j]["cd"]
                print(mu)
                for z in range(len(response[0]["mu"][j]["zon"])):
                    zon = response[0]["mu"][j]["zon"][z]["cd"]
                    print(zon)
                    for s in range(len(response[0]["mu"][j]["zon"][z]["sec"])):
                        sec = response[0]["mu"][j]["zon"][z]["sec"][s]["ns"]
                        mun_zon_sec_dump[f"{i.casefold()}"].append({"mu": mu, "zon": zon, "sec": sec})

                with open(f"{i.casefold()}.json", "w") as f:
                    json.dump(mun_zon_sec_dump, f, indent=4)

    def get_hash_mun_zon_sec(self):

        for uf in self.lista_siglas:
            with open(f"mun_zon_sec_dump/{uf}.json", "r") as f:
                mun_zon_sec_dump = json.load(f)

                for i in mun_zon_sec_dump[f"{uf}"]:
                    url = f"{self.base_url}/arquivo-urna/406/dados/{uf}/{i['mu']}/{i['zon']}/{i['sec']}/p000406-{uf}-m{i['mu']}-z{i['zon']}-s{i['sec']}-aux.json"
                    
                    response = self.get(url).json()["hashes"]
                    hash = response[0]["hash"]
                    for j in range(len(response[0]["nmarq"])):
                        if response[0]["nmarq"][j].endswith("ez"):
                            nmarq = response[0]["nmarq"][j]
                            self.get_hashes(f"{uf}", i["mu"], i["zon"], i["sec"], hash, nmarq)

    def get_hashes(self, sigla_estado, cd_municipio, cd_zona, cd_secao, hash, nmarq: str):
        url = f"{self.base_url}/arquivo-urna/406/dados/{sigla_estado}/{cd_municipio}/{cd_zona}/{cd_secao}/{hash}/{nmarq}"
        log_path = f"downloads/{sigla_estado}/{cd_municipio}/{cd_zona}/{cd_secao}"
        log_path_extracted = f"downloads/{sigla_estado}/{cd_municipio}/{cd_zona}/{cd_secao}/{nmarq}.dat"
        if not os.path.exists(f"downloads/{sigla_estado}/{cd_municipio}/{cd_zona}/{cd_secao}"):
            os.makedirs(f"downloads/{sigla_estado}/{cd_municipio}/{cd_zona}/{cd_secao}")

        # url = "https://resultados.tse.jus.br/oficial/ele2022/arquivo-urna/406/dados/go/92010/0087/0074/43304f4c543738743847325567706b2d53525a6965734b2b2d37654e597145707a5567567a6e67594b72553d/o00406-9201000870074.logjez"
        response = self.get(url)
        # path = "dowloads/o00406-9201000870074.logjez"
        with open(os.path.join(log_path, nmarq), "wb") as f:
            f.write(response.content)
            Archive(os.path.join(log_path, nmarq)).extractall(log_path)
            p = Path(log_path + "/" + "logd.dat")
            p.rename(log_path_extracted)

