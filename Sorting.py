from glob import glob
import argparse
import subprocess
import re, os

parser = argparse.ArgumentParser(description="数据集一键整理")
parser.add_argument("-ver","--version", type=str, help="版本", required=True)
parser.add_argument("-lang","--language", type=str, help="语言（可选CHS/JA/EN/KR）", required=True)
args = parser.parse_args()

lang = args.language
ver = args.version

def is_in(full_path, regx):
    if re.findall(regx, full_path):
        return True
    else:
        return False

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
            lang_code = os.path.basename(langs).replace(".json","")
            support_langs.append(lang_code)
        return support_langs
    else:
        print("不支持的版本")
        exit()
    
def get_path_by_lang(lang):
    langcodes = get_support_lang(ver)
    try:
        langcodes.index(lang)
        lang_code = lang
    except:
        print("不支持的语言")
        exit()
    return lang_code

lang_code = get_path_by_lang(lang)

def run_commands(commands):
    for i, command in enumerate(commands):
        process = subprocess.Popen(command,shell=True)
        process.wait()

# 指令列表
commands = [
    f'echo 1. 正在进行解包...', 
    f'python 1_Unpack.py -v {ver}', 
    f'echo 2. 正在整理并生成文件索引...',
    f'python 2_Sorting.py -v {ver} -l {lang_code}',
    f'echo 3. 正在生成标注...',
    f'python 3_Get_Label.py -l {lang_code}',
    f'echo 4. 正在转码语音，该步骤需要较长时间，请耐心等待...',
    f'python 4_Wem_to_Wav.py -l {lang_code}',
    f'echo 5. 正在二次分类语音...',
    f'python 5_Second_Sorting.py -l {lang_code}',
    f'echo 解包、分类完成！'
    ]

# 运行指令
run_commands(commands)