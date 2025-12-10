import os
def save_markdown(repo_path, filename, content):
    out_dir = os.path.join(repo_path, "outputs")
    os.makedirs(out_dir, exist_ok=True)
    out_file = os.path.join(out_dir, filename)
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(content)
    return out_file
