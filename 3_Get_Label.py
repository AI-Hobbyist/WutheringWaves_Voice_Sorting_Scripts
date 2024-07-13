import json
from pathlib import Path
import argparse
import os
from tqdm import tqdm
        
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

def create_label(data_dir, index_dir):
    index_file = Path(index_dir).read_text(encoding='utf-8')
    index = json.loads(index_file)
    for key in tqdm(index,desc="正在生成语音标注..."):
        for i in range(len(index[key])):
            text = index[key][i]['text']
            label = index[key][i]['file_path'].replace('.wem','.lab')
            Path(f"{data_dir}/{label}").write_text(text, encoding='utf-8')

if __name__ == "__main__":
    current_dir = os.getcwd()
    parser = argparse.ArgumentParser()
    parser.add_argument("-d","--data_dir",help="语音数据文件夹路径",default=f"{current_dir}/Data/sorted",type=str)
    parser.add_argument("-l","--lang",help="语言",required=True,type=str)
    args = parser.parse_args()
    
    data_dir = args.data_dir
    lang = args.lang.upper()
    dest_path = get_path_by_lang(lang)
    create_label(f"{data_dir}/{dest_path}", f"{data_dir}/{dest_path}/index.json")
    

