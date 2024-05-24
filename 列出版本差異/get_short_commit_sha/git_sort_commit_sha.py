import os
import subprocess


# chcp 65001 , Unicode
os.system("chcp 65001")
os.system("chcp")

# 獲取當前工作目錄
current_directory = os.getcwd()


def main():
    
    # 切换工作目录
    new_dir = r"D:\git_clone\TEAMModelOS"
    os.chdir(new_dir)

    import subprocess
    from datetime import datetime, timedelta

    # 获取当前日期和一星期前的日期
    current_date = datetime.now()
    one_week_ago_date = current_date - timedelta(days=7)

    # 将日期格式化为 Git log 中的格式
    current_date_str = current_date.strftime("%Y-%m-%d")
    one_week_ago_date_str = one_week_ago_date.strftime("%Y-%m-%d")

    # 指定目录
    directory = "TEAMModelOS"

    # 使用 Git 命令获取一星期前的提交的短哈希值（仅限定在指定目录下）
    one_week_ago_commit_sha = subprocess.check_output(
        ["git", "log", "-1", "--pretty=format:%h", "--since", one_week_ago_date_str, "--until", current_date_str, "--", directory]
    ).strip().decode("utf-8")

    # 使用 Git 命令获取最新的提交的短哈希值（仅限定在指定目录下）
    latest_commit_sha = subprocess.check_output(
        ["git", "log", "-1", "--pretty=format:%h", "--", directory]
    ).strip().decode("utf-8")

    # 打印一星期前的提交的短哈希值和最新的提交的短哈希值
    print("One week ago commit:", one_week_ago_commit_sha)
    print("Latest commit:", latest_commit_sha)


    # 切换原工作目录  
    os.chdir(current_directory)
    

if __name__ == "__main__":
    main()
    

    
   
