import os
import json
import shutil
import argparse
import re
from glob import glob
from tqdm import tqdm

def is_in(full_path, regx):
    if re.findall(regx, full_path):
        return True
    else:
        return False

def is_file(full_path):
    if os.path.exists(full_path):
        return True
    else:
        return  False

def get_support_ver():
    indexs = glob('./Indexs/*')
    support_vers = []
    for vers in indexs:
        version = os.path.basename(vers)
        support_vers.append(version)
    versions = '|'.join(support_vers)
    return versions


def get_support_lang(version):
    if is_in(version, get_support_ver()):
        support_langs = []
        indexs = glob(f'./Indexs/{version}/*')
        for langs in indexs:
            lang_code = os.path.basename(langs).replace(".json", "")
            support_langs.append(lang_code)
        return support_langs
    else:
        print("不支持的版本")
        exit()
        
def get_path_by_lang(lang):
    langcodes = get_support_lang(ver)
    path = ['中文 - Chinese', '英语 - English',  '日语 - Japanese', '韩语 - Korean']
    lang_prefix = ['zh_vo_', 'en_vo_', 'ja_vo_', 'ko_vo_']
    try:
        i = langcodes.index(lang)
        dest_path = path[i]
        dest_lang = lang_prefix[i]
        lang_code = lang
    except:
        print("不支持的语言")
        exit()
    return lang_code, dest_path, dest_lang


def load_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def read_name(key, data):
    real_name = data[key]
    return real_name
    

def copy_files(source_dir, dest_dir, file_mapping, real_file_name, real_lang):
    for root, _, files in tqdm(os.walk(source_dir),desc="正在整理并生成文件索引..."):
        for file in files:
            if file.endswith('.wem'):
                base_name = os.path.basename(file).replace('.wem', '')
                if base_name.isdigit():
                    key = int(base_name)
                else:
                    key = base_name[6:]
                
                if key in file_mapping:
                    who_id, text = file_mapping[key]
                    
                elif not isinstance(key, int):
                    if (key.endswith('_F') or key.endswith('_M')):
                        key = key[:-2]  # 去掉尾巴再查找
                        if key in file_mapping:
                            who_id, text = file_mapping[key]
                        else:
                            tqdm.write(f"未找到文件 {file} 对应的文本")
                            continue
                    else:
                        tqdm.write(f"未找到文件 {file} 对应的文本")
                        continue
                else:
                    tqdm.write(f"未找到文件 {file} 对应的文本")
                    continue
                dest_subdir = os.path.join(dest_dir, who_id.replace('?', '？'))
                os.makedirs(dest_subdir, exist_ok=True)
                dest_path = os.path.join(dest_subdir, file)
                name = os.path.basename(file).replace('.wem', '')
                if isinstance(name, int) or name.isdigit():
                    real_name = f"{real_lang}{read_name(key, real_file_name)}"
                    dest_path = dest_path.replace(name, real_name)
                shutil.copyfile(os.path.join(root, file), dest_path)
                result[who_id].append({"text": text, "file_path": os.path.relpath(dest_path, dest_dir)})

def create_file_mapping(data):
    file_mapping = {}
    for entry in data:
        tid_talk = entry['TidTalk']
        file_mapping[tid_talk] = (entry['WhoId'], entry['Text'])
    return file_mapping

def get_real_filename(data):
    mapping = {}
    for entry in data:
        tid_talk = entry['TidTalk']
        if isinstance(tid_talk, int):
            file_name = entry['FileName']
            mapping[tid_talk] = file_name
    return mapping

if __name__ == "__main__":
    current_dir = os.getcwd()
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--src", help="源目录", default=f'{current_dir}/Data/paks', type=str)
    parser.add_argument("-v", "--version", help="版本", required=True, type=str)
    parser.add_argument("-l", "--lang", help="语言", required=True, type=str)
    parser.add_argument("-o", "--output", help="输出目录", default=f'{current_dir}/Data/sorted', type=str)
    args = parser.parse_args()
    
    src = args.src
    ver = args.version
    language = args.lang.upper()
    dest = args.output
    
    langcode, dest_lang, real_lang = get_path_by_lang(language)
    # 读取JSON数据
    json_data = load_json(f'{current_dir}/Indexs/{ver}/{langcode}.json')

    # 创建文件映射
    file_mapping = create_file_mapping(json_data)
    real_file_name = get_real_filename(json_data)
    # 初始化结果字典
    result = {entry['WhoId']: [] for entry in json_data}

    # 复制文件并生成结果
    copy_files(src, f"{dest}/{dest_lang}", file_mapping, real_file_name, real_lang)

    result = {who_id: texts for who_id, texts in result.items() if texts}

    # 输出结果为JSON文件
    with open(os.path.join(f"{dest}/{dest_lang}",'index.json'), 'w', encoding='utf-8') as outfile:
        json.dump(result, outfile, ensure_ascii=False, indent=4)