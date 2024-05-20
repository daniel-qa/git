# -*- coding: utf-8 -*-
from opencc import OpenCC

# 初始化 OpenCC 转换器
cc = OpenCC('s2t')  # 简体到繁体

# 判断字符是否是简体和繁体相同
def is_not_simplified_and_traditional_same(char):
    traditional_char = cc.convert(char)
    return not char == traditional_char


# 判斷字串是否有簡體字，則排除，會排除與繁體字共用的部分
def is_gb2312_char(char):
    try:
        # 尝试将字符编码为 GB2312
        char.encode('gb2312')
        return True
    except UnicodeEncodeError:
        return False

def contains_simplified_chinese(string):
    for char in string:
        if '\u4e00' <= char <= '\u9fff' and is_gb2312_char(char) and is_not_simplified_and_traditional_same(char):        
            return True
    return False

def append_string_to_file(string, file_path="log.txt"):
    with open(file_path, 'a', encoding='utf-8') as file:
        file.write(string + '\n')

# 示例字符串数组
test_strings = [
    '测试文字档案！',  # 全部是简体字
    '時間',  # 全部是繁体字,並且沒有與簡體共用
    '我是',  # 全部是繁体字,並與簡體共用
    'Hello, World!',  # 英文
    '简体和繁體混合'  # 混合
]


if __name__ == "__main__":

    # 检查字符串数组
    for test_string in test_strings:
        if contains_simplified_chinese(test_string):
            print(f"字符串 '{test_string}' 包含简体字")
            append_string_to_file(test_string)
        else:
            print(f"字符串 '{test_string}' 不包含简体字")
