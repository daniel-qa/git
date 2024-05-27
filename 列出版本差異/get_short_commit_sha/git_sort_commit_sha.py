import subprocess
from datetime import datetime, timedelta

def run_git_command(command):
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)
    if result.returncode != 0:
        raise Exception(f"Git command failed: {result.stderr}")
    return result.stdout.strip()

def get_latest_commit():
    command = "git log -1 --pretty=format:%h"
    return run_git_command(command)

def get_commit_one_week_ago():
    one_week_ago = (datetime.now() - timedelta(weeks=1)).isoformat()
    command = f"git log -1 --before='{one_week_ago}' --pretty=format:%h"
    return run_git_command(command)

if __name__ == "__main__":
    try:
        latest_commit = get_latest_commit()
        commit_one_week_ago = get_commit_one_week_ago()
        print(f"Latest commit: {latest_commit}")
        print(f"Commit one week ago: {commit_one_week_ago}")
    except Exception as e:
        print(f"Error: {e}")
