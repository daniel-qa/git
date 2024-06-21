# -*- coding: utf-8 -*-
import re
from collections import Counter
import opencc

def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    return content

def find_single_quoted_strings(content):
    # 使用正則表達式找到所有單引號內的字串
    pattern = r"'([^']*)'"
    matches = re.findall(pattern, content)
    return matches

def write_output(strings, output_path):
    with open(output_path, 'w', encoding='utf-8') as file:
        for string in strings:
            file.write(f"{string}\n")

def are_traditional_and_simplified_same(text):
    converter = opencc.OpenCC('t2s.json')
    simplified = converter.convert(text)
    converter = opencc.OpenCC('s2t.json')
    traditional = converter.convert(simplified)
    return text == traditional

def find_string_main():
    input_file = "IES5 找到中文字串.txt"
    output_file = "找到相同的翻譯字串.txt"
    
    # 讀取文件內容
    content = read_file(input_file)
    
    # 找到所有單引號內的字串
    quoted_strings = find_single_quoted_strings(content)
    
    # 計算每個字串出現的次數
    string_counts = Counter(quoted_strings)
    
    # 過濾出現過兩次且簡繁相同的字串
    repeated_strings = [
        string for string, count in string_counts.items()
        if count = 2 and not are_traditional_and_simplified_same(string)
    ]
    
    # 將結果寫入輸出文件
    if not repeated_strings :
        print("翻譯字串表沒有找到相同字串")
        with open(output_file, 'w') as file:        
            file.write("翻譯字串表沒有找到相同字串")
    else:
        print("翻譯字串表有找到相同字串，已寫入 " +  output_file)
        write_output(repeated_strings, output_file)

if __name__ == "__main__":
    find_string_main()

    
    