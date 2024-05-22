# -*- coding: utf-8 -*-
import os
import re
import subprocess

"""
Author: Daniel
Date: 2024.05.22
Description: This script compares two Git commits, filters out specific files, and outputs lines containing Chinese characters to a log file.
"""

def contains_chinese(text):
    """Check if a string contains any Chinese characters."""
    return re.search(r'[\u4e00-\u9fff]', text) is not None

def is_excluded_line(text):
    """Check if a line should be excluded based on its starting characters."""
    excluded_starts = ['//', '#', '/*', '<!']
    return any(text.startswith(exclude) for exclude in excluded_starts)

def extract_file_info(line):
    """Extract file name from a diff line."""
    file_info = re.search(r'\+\+\+ b/(.*)', line)
    return file_info.group(1) if file_info else None

def process_diff(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    output_lines = []
    current_file = None
    current_line_number = 0

    for line in lines:
        stripped_line = line.strip()
        
        print("stripped_line :"  + stripped_line)
        
        # Track the current file being processed
        if stripped_line.startswith('+++ b/'):
            current_file = extract_file_info(stripped_line)
            current_line_number = 0
            continue

        # Track line numbers in the diff
        if stripped_line.startswith('@@'):
            line_info = re.search(r'\+(\d+)', stripped_line)
            if line_info:
                current_line_number = int(line_info.group(1)) - 1
            continue
            
        # filter start with '-' and '---'
        if stripped_line.startswith('-')  or stripped_line.startswith('---'):
            continue
        

        # Increment the line number for added lines
        if stripped_line.startswith('+') and not stripped_line.startswith('+++'):
            current_line_number += 1
            if contains_chinese(stripped_line) and not is_excluded_line(stripped_line[1:].strip()):
                output_lines.append(f"{current_file}:{current_line_number}: {line}")
        #else:
        #    # 原本存在的部分
        #    current_line_number += 1
        #    if contains_chinese(stripped_line) and not is_excluded_line(stripped_line.strip()):
        #        output_lines.append(f"{current_file}:{current_line_number}: {line}")

    with open(output_file, 'w', encoding='utf-8') as f:
        for output_line in output_lines:
            f.write(output_line)


# 直接寫入 raw_data.log
def direct_wirte_raw_data_log(file,result):
    with open(file, "w", encoding='utf-8') as file:
        #file.write("標準輸出:\n")
        file.write(result.stdout)

def git_diff_log(commit1,commit2):
    # 獲取當前工作目錄
    current_directory = os.getcwd()
    
    # 切换工作目录
    new_dir = r"D:\git_clone\TEAMModelOS"
    os.chdir(new_dir)
    
     # 比對 commit
    #commit1 = "a39a3f8352"
    #commit2 = "588443111b"
    command = f"git diff {commit1} {commit2}"  
    command = command + " -- . :(exclude)TEAMModelOS/ClientApp/public/lang"  # 排除語系檔
    command = command + " :(exclude)TEAMModelBI"  # 排除 BI專案
    command = command + " :(exclude)TEAMModelOS.FunctionV4"  # 排除 FunctionV4專案
    command = command + " :(exclude)TEAMModelOS.SDK"  # 排除 TEAMModelOS.SDK專案
    command = command + " :(exclude)TEAMModelOS.TEST"  # 排除 TEAMModelOS.TEST專案
    command = command + " :(exclude)TEAMModelOS/TEAMModelOS.csproj"  # 排除 csproj專案檔
    
    print( command)
    
    # 运行 Git 命令   
    # 执行命令并捕获输出
    #command = 'dir'
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='utf-8')
    
    # 切换原工作目录  
    os.chdir(current_directory)
    
    msg = result.stdout    
    
    # 輸出直接寫入 git_diff.log
    direct_wirte_raw_data_log("git_diff.log",result)
    

def format_log(input_file_path,output_file_path):

    #input_file_path = 'output.log'  # 替换为实际的输入文件路径
    #output_file_path = 'formatted_output.log'  # 替换为所需的输出文件路径


    # 打开输入文件进行读取
    with open(input_file_path, 'r', encoding='utf-8') as infile:
        lines = infile.readlines()

    # 初始化存储处理后的行的变量
    output_lines = []
    current_file = ''

    # 处理输入文件中的每一行
    for line in lines:
        # 使用冒号和数字分割行
        parts = line.split(':', 2)
        if len(parts) == 3:
            file_path = parts[0]
            line_number = parts[1]
            content = parts[2].strip()

            # 如果文件路径不同，或者是第一次处理，添加文件路径到输出行
            if file_path != current_file:
                if current_file:
                    output_lines.append('\n')
                current_file = file_path
                output_lines.append(current_file + '\n')

            # 添加内容到输出行
            output_lines.append(line_number + ' ' + content + '\n')
        else:
            continue

    # 打开输出文件进行写入
    with open(output_file_path, 'w', encoding='utf-8') as outfile:
        outfile.writelines(output_lines)

    print("处理后的内容已写入到", output_file_path)
    

if __name__ == "__main__":

    # chcp 65001 , Unicode
    os.system("chcp 65001")
    os.system("chcp")

    # git diff log
    commit1 = "c821ac6e3a"
    commit2 = "9c7e3b9000"
    
    git_diff_log(commit1,commit2)    

    input_file = 'git_diff.log'  # 输入文件名
    output_file = 'output.log'  # 输出文件名

    # 找出中文字，並輸出至 output.log
    process_diff(input_file, output_file)

    # 格式化 output.log ,並輸出至新檔案
    final_file = "IES5 找到中文字串.log"
    format_log(output_file,final_file)
    