# -*- coding: utf-8 -*-
import os
import subprocess
import re

def run_git_command(command):
    """运行git命令并返回输出"""
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE)
    return result.stdout


def main():
    commit1 = "6f81fbc192"
    commit2 = "fca2a8f013"
    command = f"git diff {commit1} {commit2}"

    # 运行 Git 命令
    diff_output = run_git_command(command)

    # 簡體字元
    simplified_chinese_text = extract_simplified_chinese(diff_output)

    # 将输出写入日志文件
    with open('git_diff_log.txt', 'wb') as log_file:
        log_file.write(simplified_chinese_text)

if __name__ == "__main__":
    # 切换工作目录
    new_dir = r"D:\git_clone\TEAMModelOS"
    os.chdir(new_dir)

    main()
