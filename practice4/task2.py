import json
from pathlib import Path

import git

repo_status = {}

with open("repos.txt", "r") as file:
    while line := file.readline().rstrip():
        try:
            l = line.split("/")
            repo_dir_name = l[-1].split(".")[0]
            repo_dir = Path.cwd() / repo_dir_name
            git.Git(repo_dir).clone(line)
            repo_status[line] = "OK"
        except Exception:
            repo_status[line] = "FAIL"

json.dump(repo_status, open("repo_status.json", 'w'))
