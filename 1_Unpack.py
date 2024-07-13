import argparse, subprocess, re, os
from glob import glob
from tqdm import tqdm
from pathlib import Path

current_dir = os.getcwd()

def is_in(full_path, regx):
    if re.findall(regx, full_path):
        return True
    else:
        return False

def check_supported_version():
    aes_key_file = glob("./AES_Key/*.key")
    supported_versions = []
    for key in aes_key_file:
        version = Path(key).name.replace(".key","")
        supported_versions.append(version)
    versions = "|".join(supported_versions)
    return versions
    
def unpack(src,version):
    paks = glob(f"{src}/*.pak")
    aes_key = Path(f"{current_dir}/AES_Key/{version}.key").read_text(encoding="utf-8")
    for pak in tqdm(paks,desc="正在解包..."):
        subprocess.run(f"{current_dir}/Tools/repak/repak.exe -a {aes_key} unpack \"{pak}\"")
        
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-s","--src",help="需要解包的文件夹路径",default=f"{current_dir}/Data/paks",type=str)
    parser.add_argument("-v","--version",help=f"支持的版本为：{check_supported_version()}",required=True,type=str)
    args = parser.parse_args()
    if is_in(args.version,check_supported_version()):
        unpack(args.src,args.version)
    else:
        print(f"不支持的版本{args.version}")
        exit()