import json, re, os, argparse
from tqdm import tqdm
from pathlib import Path
from glob import glob
from shutil import move

current_path = os.getcwd()

parser = argparse.ArgumentParser()
parser.add_argument('-src','--source', type=str, help='待二次分类数据集', default=f"{current_path}/Data/sorted")
parser.add_argument('-dst','--destination', type=str, help='目标路径', default=f"{current_path}/Data/sorted")
parser.add_argument('-l','--lang', type=str, help='语言', required=True)
args = parser.parse_args()

source = str(args.source)
dest = str(args.destination)
lang = str(args.lang)
monster = 'monster'
battle = 'battle|life|atk|skill|hp70|hp50|hp30|die|summon|qte'
conv = 'fetter'
vaild_content = r'[a-zA-Z0-9\u4e00-\u9fa5\u3040-\u309f\u30a0-\u30ff\u1100-\u11ff\u3130-\u318f\uac00-\ud7af]+'
placeholder = r'[{}]'
tags = r'[<>]'

def is_in(full_path, regx):
    if re.findall(regx, full_path):
        return True
    else:
        return False
    
def check(full_path, regx):
    if re.findall(regx, full_path):
        return True
    else:
        return False
    
def check_content(text, regx):
    if re.search(regx, text):
        return True
    else:
        return False
    
def tag_content(text):
    res = re.findall(r'(<.*?>)', text)
    string = '、'.join(res)
    return string

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

path_by_lang= get_path_by_lang(lang.upper())
labfiles = glob(f"{source}/{path_by_lang}/**/*.lab")

for file in tqdm(labfiles):
    try:
        lab_content = Path(file).read_text(encoding='utf-8')
        spk = os.path.basename(os.path.dirname(file))
        lab_file_name = os.path.basename(file)
        wav_file_name = lab_file_name.replace(".lab",".wav")
        src = f"{source}/{path_by_lang}/{spk}"
        if check_content(lab_content,tags):
            labels = re.sub(r'<.*?>', '', lab_content)
            lab_path = f"{src}/{path_by_lang}/{lab_file_name}"
            Path(lab_path).write_text(labels,encoding='utf-8')
            tqdm.write(f"已清除标注文件 {src}/{lab_file_name} 中的html标签：{tag_content(lab_content)}\n-----------")
        if not check_content(lab_content,vaild_content):
            out_path = f"{dest}/{path_by_lang}/{spk}/其它语音 - Others"
        elif is_in(file,conv):
            out_path = f"{dest}/{path_by_lang}/{spk}/多人对话 - Conversation" 
        elif check_content(lab_content,placeholder):
            out_path = f"{dest}/{path_by_lang}/{spk}/带变量语音 - Placeholder"
        elif is_in(file,monster):
            out_path = f"{dest}/{path_by_lang}/{spk}/怪物语音 - Monster"
        elif is_in(file,battle):
            out_path = f"{dest}/{path_by_lang}/{spk}/战斗语音 - Battle"
        else:
            continue
        if not os.path.exists(out_path):
            Path(f"{out_path}").mkdir(parents=True)
        move(f"{src}/{lab_file_name}",f"{out_path}/{lab_file_name}")
        move(f"{src}/{wav_file_name}",f"{out_path}/{wav_file_name}")
        tqdm.write(f"音频文件：{src}/{wav_file_name}\n标注文件：{src}/{lab_file_name}\n已移动至：{out_path}\n-----------")
    except:
        pass

    
