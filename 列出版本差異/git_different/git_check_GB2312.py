# -*- coding: utf-8 -*-
import os
import subprocess
import re
from check_GB2312 import contains_simplified_chinese

# 寫入 Log 檔
def append_string_to_file(string, file_path="log.txt"):
    with open(file_path, 'a', encoding='utf-8') as file:
        file.write(string + '\n')

def main():

    # chcp 65001
    os.system("chcp 65001")
    os.system("chcp")

    commit1 = "6f81fbc192"
    commit2 = "fca2a8f013"
    command = f"git diff {commit1} {commit2}"
    
    # 运行 Git 命令   
    # 执行命令并捕获输出
    #command = 'dir'
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='utf-8')
    
    # 输出结果
    #print('Exit status:', result.returncode)
    #print('Standard Output:\n\n', result.stdout)
    #print('Standard Error:', result.stderr)

    # 读取并分割输出
    output_lines = result.stdout
    
    #print(type(output_lines))

    # 逐行处理输出
    for line in output_lines.split("\n"):
        print('Line is:' + str(line) )

        # 对每一行做你需要的处理
        # 檢是是否有簡體字
        if contains_simplified_chinese(line.strip()):
            print(f"字符串 '{line}' 包含简体字")
            append_string_to_file(line.strip())


if __name__ == "__main__":
    # 切换工作目录
    new_dir = r"D:\git_clone\TEAMModelOS"
    os.chdir(new_dir)

    main()
