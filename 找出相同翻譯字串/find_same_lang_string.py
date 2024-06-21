# -*- coding: utf-8 -*-
import os,sys
import re
import subprocess
from datetime import datetime, timedelta

"""
Author: Daniel
Date: 2024.06.21
Description: This script compares two specified Git commits within a designated folder, 
identifies identical Chinese strings, and logs the results to a text file.
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


#  找出中文字，過濾註解，並輸出至  output.log
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
        
        # filter lines that contain 'SendBotMsg' or 'console.log'
        if 'SendBotMsg' in stripped_line or 'console.log' in stripped_line:
            continue

        # filter * 页面滚动事件
        # 檢查是否以 "+" 或 "-" 開頭
        input_str = stripped_line
        if input_str.startswith('+') or input_str.startswith('-'):
            # 移除 "+" 或 "-" 號後的空白
            input_str = input_str[1:].lstrip()
            # 移除 "+" 或 "-" 號
            input_str = input_str.lstrip('+-')
            # 檢查是否以 "* " 開頭
            if input_str.startswith('* '):
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

# 產出 git_diff.log 
def git_diff_log(commit1,commit2):
    # 獲取當前工作目錄
    current_directory = os.getcwd()
    
    # 切换工作目录
    new_dir = r"D:\git_clone\TEAMModelOS"
    os.chdir(new_dir)
    
     # 比對 commit
    #commit1 = "a39a3f8352"
    #commit2 = "588443111b"
    #command = f"git diff {commit1} {commit2}"  
    #command = command + " -- . :(exclude)TEAMModelOS/ClientApp/public/lang"  # 排除語系檔
    #command = command + " :(exclude)TEAMModelOS/Lang"  # 排除語系檔
    #command = command + " :(exclude)TEAMModelBI"  # 排除 BI專案
    #command = command + " :(exclude)TEAMModelOS.FunctionV4"  # 排除 FunctionV4專案
    #command = command + " :(exclude)TEAMModelOS.SDK"  # 排除 TEAMModelOS.SDK專案
    #command = command + " :(exclude)TEAMModelOS.TEST"  # 排除 TEAMModelOS.TEST專案
    #command = command + " :(exclude)TEAMModelOS/TEAMModelOS.csproj"  # 排除 csproj專案檔
    #command = command + " :(exclude)TEAMModelContest"  # 排除 csproj專案檔
    
    
    # 指定查詢翻譯字串表
    command = f"git diff {commit1} {commit2}"  
    command = command + " TEAMModelOS/ClientApp/public/lang"  # 排除語系檔
    
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

def run_git_command(command):
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)
    if result.returncode != 0:
        raise Exception(f"Git command failed: {result.stderr}")
    return result.stdout.strip()

def get_latest_commit():
    #command = "git log -1 --pretty=format:%h"
    command = "git log -1 --pretty=format:%h --abbrev=10"
    return run_git_command(command)

def get_commit_one_day_ago():
    one_day_ago = (datetime.now() - timedelta(days=1)).isoformat()
    command = f"git log -1 --before='{one_day_ago}' --pretty=format:%h --abbrev=10"
    return run_git_command(command)
    
def get_commit_three_days_ago():
    three_days_ago = (datetime.now() - timedelta(days=3)).isoformat()
    command = f"git log -1 --before='{three_days_ago}' --pretty=format:%h --abbrev=10"
    return run_git_command(command)

def get_commit_five_days_ago():
    three_days_ago = (datetime.now() - timedelta(days=5)).isoformat()
    command = f"git log -1 --before='{three_days_ago}' --pretty=format:%h --abbrev=10"
    return run_git_command(command)

def get_commit_one_week_ago():
    one_week_ago = (datetime.now() - timedelta(weeks=1)).isoformat()
    command = f"git log -1 --before='{one_week_ago}' --pretty=format:%h --abbrev=10"
    return run_git_command(command)
 
def get_commit_two_weeks_ago():
    two_weeks_ago = (datetime.now() - timedelta(weeks=2)).isoformat()
    command = f"git log -1 --before='{two_weeks_ago}' --pretty=format:%h --abbrev=10"
    return run_git_command(command) 

def get_commit_one_month_ago():
    one_month_ago = (datetime.now() - timedelta(days=30)).isoformat()
    command = f"git log -1 --before='{one_month_ago}' --pretty=format:%h --abbrev=10"
    return run_git_command(command)

def my_function(param1, param2):
    print(f"Function executed with parameters: {param1} and {param2}")

                    
if __name__ == "__main__":

    # chcp 65001 , Unicode
    os.system("chcp 65001")
    os.system("chcp")

    # 獲取當前工作目錄
    current_directory = os.getcwd()
    
    
    if len(sys.argv) == 3:  # 期望有两个参数
        param1 = sys.argv[1]
        param2 = sys.argv[2]
        my_function(param1, param2)
        
    
    if(1):    
    
        # 切换工作目录
        new_dir = r"D:\git_clone\TEAMModelOS"
        os.chdir(new_dir)    
        # 要設定跟蹤遠端 branch
        os.system("git branch --set-upstream-to=origin/develop develop")    
        # git pull
        os.system("git pull")
        

        # 取得最新 commit ，及一星期前的一個 commit 
        latest_commit = get_latest_commit()
        commit_one_week_ago = get_commit_one_week_ago()
        #commit_one_week_ago = get_commit_five_days_ago()
        #commit_one_week_ago = get_commit_two_weeks_ago()
        
        
        
        print(f"Latest commit: {latest_commit}")
        print(f"Commit one week ago: {commit_one_week_ago}")

        # 切换原工作目录  
        os.chdir(current_directory)
        
        if(1):

            # git diff log
            #commit1 = "794355bcb5"
            #commit2 = "ca6091003b"
            
            commit1 = commit_one_week_ago 
            commit2 = latest_commit
            
            
            input_file = 'git_diff.log'  # 输入文件名
            output_file = 'output.log'  # 输出文件名
        
            # 產生 git diff  raw data
            git_diff_log(commit1,commit2)
            
            if(1):
            
                # 找出中文字，並輸出至 output.log
                process_diff(input_file, output_file)
                
                # 檢查有後來刪除的中文字，並過濾(Pending)
                
                # 格式化 output.log ,並輸出至新檔案
                final_file = "IES5 找到中文字串.txt"
                format_log(output_file,final_file)
                
                

    # 找出多語字串相同的的字串
    if(1):
        import check_same_multi_lang_string     
        # 處理字串並輸出結果
        check_same_multi_lang_string.find_string_main()

    
