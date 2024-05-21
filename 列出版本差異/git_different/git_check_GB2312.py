# -*- coding: utf-8 -*-
import os
import datetime
from datetime import datetime, timedelta
import subprocess
import re
from check_GB2312 import contains_simplified_chinese


'''
比對兩個 commit 之間的差異，分析有簡體字的部分

1. 只有簡體字，不含註解
2. 有簡體字，包含註解
3. raw data
'''

# 寫入 Log 檔
def append_string_to_file(string, file_path="GB_log.log"):
    with open(file_path, 'a', encoding='utf-8') as file:
        file.write(string + '\n')

# 直接寫入 raw_data.log
def direct_wirte_raw_data_log(result):
    with open("raw_data.log", "w", encoding='utf-8') as file:
        file.write("標準輸出:\n")
        file.write(result.stdout)
    

def main():

    # chcp 65001 , Unicode
    os.system("chcp 65001")
    os.system("chcp")


    # 比對 commit
    commit1 = "a39a3f8352"
    commit2 = "588443111b"
    command = f"git diff {commit1} {commit2}"  
    command = command + " -- . :(exclude)TEAMModelOS/ClientApp/public/lang"  # 排除語系檔
    
    
    # 运行 Git 命令   
    # 执行命令并捕获输出
    #command = 'dir'
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='utf-8')
    
    # 切换原工作目录  
    os.chdir(current_directory)
    
    # 輸出直接寫入 raw_data.log
    direct_wirte_raw_data_log(result)    
    
    
    ## 只寫入有簡體字的部分; 直接對照 rawdata log 即可
    #if(0):
    #    # 读取并分割输出
    #    output_lines = result.stdout
    #    
    #    #print(type(output_lines))
    #    
    #    # 逐行处理输出
    #    for line in output_lines.split("\n"):
    #        #print('Line is:' + str(line) )
    #    
    #        # 对每一行做你需要的处理
    #        # 檢是是否有簡體字
    #        if contains_simplified_chinese(line.strip()):
    #            print(f"字符串 '{line}' 包含简体字")
    #            append_string_to_file(line.strip())
                
                
    # 只寫入有簡體字的部分，並過慮掉註解和 console log
    if(1):
        # 读取并分割输出
        output_lines = result.stdout
       
        # 逐行处理输出
        for line in output_lines.split("\n"):
            
            #print('Line is:' + str(line) )
            
            # 对每一行做你需要的处理
            
            # 是註解，直接過濾
            stripped_line = line.strip()  # 先去掉前後空白
            
            # 過濾條件
            if(
                stripped_line.startswith('//') or
                stripped_line.startswith('#') or
                stripped_line.startswith('/*') or
                stripped_line.startswith('<!') or
                'console.log(' in stripped_line or
                'console.error(' in stripped_line or
                stripped_line.startswith('-')
            ):
                continue
                        
            
            # 檢是是否有簡體字
            if contains_simplified_chinese(line.strip()):
                print(f"字符串 '{line}' 包含简体字")
                
                # 過濾註解
                stripped_line = line.strip()  # 先去掉前後空白
                
                if stripped_line.startswith('+') or stripped_line.startswith('-'):
                    
                    # 去掉空白
                    stripped_line2 = stripped_line[1:].strip()
                    
                    # 去掉 TAB
                    stripped_line2=  stripped_line2.lstrip('\t')
                    
                    # 過濾掉以 // 或 # 開頭的行,及前後空白
                    
                    # 開頭是註解的話，則過濾
                    if stripped_line2.startswith('//') or stripped_line2.startswith('#')  or stripped_line2.startswith('/*') or stripped_line2.startswith('<!') :
                        pass
                    else:                
                        append_string_to_file(line.strip(),"GB_filter_annotation.log")
                else:
                    append_string_to_file(line.strip(),"GB_filter_annotation.log")
        

if __name__ == "__main__":

    # 獲取當前工作目錄
    current_directory = os.getcwd()

    # 清除 log
    
    os.system("del GB_filter_annotation.log")
    os.system("del GB_log.log")
    
    
    # 切换工作目录
    new_dir = r"D:\git_clone\TEAMModelOS"
    os.chdir(new_dir)
    
    main()
