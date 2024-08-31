import requests
import re
import cfg

def parse_files_dirs(xml_str : str) -> list:
    #sorry....

    #i could do
    regex = re.compile("<(Prefix|Key)>([a-zA-Z0-9-/\\.]*)</(Prefix|Key)>")
    res_strs = regex.findall(xml_str)
    res = []
    for res_tup in res_strs[1:]:
        res.append(res_tup[1])
    return res


def fetch_files_dirs(path) -> list:
    res = requests.get(cfg.api_url + "?delimiter=/&prefix=" + path, proxies=cfg.proxies)
    return parse_files_dirs(res.content.decode())

def filter_archives_only(files : list) -> list:
    return list(filter(lambda x : x.endswith(".zip"), files))

def filter_year(files : list, years : list) -> list:
    def filter_fn(x):
        for year in years:
            if year in x:
                return False
        return True
    return list(filter(filter_fn, files))

#TODO: handle request errors
def fetch_and_save_archives(files : list):
    for fpath in files:
        fname = fpath.split("/")[-1]
        res = requests.get(cfg.files_url + fpath)
        with open(f"{cfg.temp_dir}/{fname}", "wb+") as f:
            f.write(res.content)
    

