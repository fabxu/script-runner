import os
# git client to pull the code
class RepoClient:
    def __init__(self):
        pass

    def pull(self, url, target_dir="."):
        cmd = f"git clone {url} {target_dir}"
        os.system(cmd)

    def if_successful(self, repo_name, target_dir="."):
        return os.path.exists(os.path.join(target_dir, repo_name))