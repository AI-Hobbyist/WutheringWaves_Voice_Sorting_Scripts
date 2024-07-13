import os,subprocess,argparse
from glob import glob
from tqdm import  tqdm
from pathlib import Path

current_dir = os.getcwd()

def get_path_by_lang(lang):
    langcodes = ["CHS","EN","JA","KR"]
    path = ['中文 - Chinese', '英语 - English',  '日语 - Japanese', '韩语 - Korean']
    try:
        i = langcodes.index(lang)
        dest_path = path[i]
    except:
        print("不支持的语言")
        exit()
    return dest_path

def to_wav(src):
    wem_file = glob(f"{src}/**/*.wem")
    for wems in tqdm(wem_file,desc="正在转码音频，请耐心等待完成..."):
        wav_path = wems.replace(".wem",".wav")
        subprocess.run(f"{current_dir}/Tools/vgmstream/vgmstream-cli.exe -o \"{wav_path}\" \"{wems}\"",stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
        Path(wems).unlink()
    tqdm.write(f"转码完成！")
        
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-s","--src",help="需要转码的文件夹路径",default=f"{current_dir}/Data/sorted",type=str)
    parser.add_argument("-l","--lang",help="语言",required=True,type=str)
    args = parser.parse_args()
    
    dest_path = get_path_by_lang(args.lang.upper())
    to_wav(f"{args.src}/{dest_path}")