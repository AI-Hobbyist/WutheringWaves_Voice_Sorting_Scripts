import os,subprocess,argparse, multiprocessing
from glob import glob
from os import cpu_count
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
    wav_path = str(Path(src)).replace(".wem",".wav")
    if not Path(wav_path).exists():
        subprocess.run(f"{current_dir}/Tools/vgmstream/vgmstream-cli.exe -o \"{wav_path}\" \"{src}\"",stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
        Path(src).unlink()

def conv_wem_to_wav(process_count, wem):
    if process_count == 0:
        process_count = cpu_count()
    files = glob(f"{wem}/**/*.wem")
    file_count = len(files)

    with tqdm(total=file_count, desc="正在转码音频，请耐心等待完成...") as progress_bar:
        with multiprocessing.Pool(process_count) as pool:
            for result in pool.imap_unordered(to_wav, files):
                progress_bar.update(1)
        
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-s","--src",help="需要转码的文件夹路径",default=f"{current_dir}/Data/sorted",type=str)
    parser.add_argument("-p","--process",help="进程数",default=0,type=int)
    parser.add_argument("-l","--lang",help="语言",required=True,type=str)
    args = parser.parse_args()
    
    dest_path = get_path_by_lang(args.lang.upper())
    conv_wem_to_wav(args.process, f"{args.src}/{dest_path}")