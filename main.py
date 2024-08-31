import os
import zipfile
import shutil
import scraper
import cfg
import sys
def clean_temp():
    if os.path.isdir(cfg.temp_dir):
        shutil.rmtree(cfg.temp_dir)
    os.mkdir(cfg.temp_dir)
def mkdir_if_not_exist(dir):
    if not os.path.isdir(dir):
        os.makedirs(dir)
    
def extract_archive(fname : str) -> bytes:
    csv_name = fname.split(".")[0] + ".csv"
    with zipfile.ZipFile(cfg.temp_dir + "/" + fname, "r") as arch:
        data = arch.read(csv_name)
    return data

def extract_header(fname : str) -> str:
    dat = str(extract_archive(fname), "utf-8")
    return dat.split("\n")[0]
    
def extract_body(fname : str) -> list:
    dat = str(extract_archive(fname), "utf-8")
    #check if header is present
    dat_lines = dat.split("\n")[:-1]
    if dat_lines[0].split(",")[0].isnumeric():
        return dat_lines
    return dat_lines[1:]

def get_csv_name(archive_name : str) -> str:
    arch_split = archive_name.split("-")
    return f"{arch_split[0]}-{arch_split[1]}"

def line_is_clean(line : str):
    if "0.00000000" in line:
        return False
    return True
klines_path = "data/spot/monthly/klines/"


def main():
    coin_name = sys.argv[1]
    if coin_name == None:
        coin_name = "BTCS"
    cfg.temp_dir = coin_name

    files = scraper.fetch_files_dirs(klines_path + coin_name + "USDT/5m/")
    archs = scraper.filter_archives_only(files)
    archs = scraper.filter_year(archs, ["2017", "2018", "2019"])
    clean_temp()
    scraper.fetch_and_save_archives(archs)
    mkdir_if_not_exist("data")

    dirs = os.listdir(cfg.temp_dir)
    dirs.sort()
    #out = extract_header(dirs[0]) + "\n"
    out = cfg.header + "\n"
    for file in dirs:
        
        for line in extract_body(file):
            if not line_is_clean(line):
                continue
            out += line + "\n"
    with open(f"data/{get_csv_name(dirs[0])}.csv", "w+") as f:
        f.write(out)    
    clean_temp()


main()