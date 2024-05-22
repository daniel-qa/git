# -*- coding: utf-8 -*-
import os
import subprocess


# 直接寫入 raw_data.log
def direct_wirte_raw_data_log(file,result):
    with open(file, "w", encoding='utf-8') as file:
        file.write("標準輸出:\n")
        file.write(result.stdout)
    

if __name__ == "__main__":
    
    # chcp 65001 , Unicode
    os.system("chcp 65001")
    os.system("chcp")

    # 獲取當前工作目錄
    current_directory = os.getcwd()
    
    # 切换工作目录
    new_dir = r"D:\git_clone\TEAMModelOS"
    os.chdir(new_dir)
    
    # 比對 commit
    commit1 = "a39a3f8352"
    commit2 = "588443111b"
    command = f"git diff {commit1} {commit2}"  
    command = command + " -- . :(exclude)TEAMModelOS/ClientApp/public/lang"  # 排除語系檔
    
    print( command)
    
    # 运行 Git 命令   
    # 执行命令并捕获输出
    #command = 'dir'
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='utf-8')
    
    # 切换原工作目录  
    os.chdir(current_directory)
    
    msg = result.stdout
    
    #print(msg)
    
    # 輸出直接寫入 git_diff.log
    direct_wirte_raw_data_log("git_diff.log",result)    
    