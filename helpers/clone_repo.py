from git import Repo
import os
def clone_repository(repo_url, out_base="./outputs"):
    repo_name = repo_url.rstrip("/").split("/")[-1].replace(".git", "")
    clone_path = os.path.join(out_base, repo_name)
    os.makedirs(out_base, exist_ok=True)
    if not os.path.exists(clone_path):
        Repo.clone_from(repo_url, clone_path)
    return os.path.abspath(clone_path)
