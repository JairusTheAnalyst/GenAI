import os, json
IGNORED = {'.git', 'node_modules', '__pycache__'}

def build_file_tree(root_path):
    def walk(dirpath):
        tree = {"path": dirpath, "files": [], "dirs": []}
        try:
            for entry in sorted(os.listdir(dirpath)):
                if entry in IGNORED:
                    continue
                full = os.path.join(dirpath, entry)
                if os.path.isdir(full):
                    tree["dirs"].append(walk(full))
                else:
                    tree["files"].append(entry)
        except PermissionError:
            pass
        return tree
    return walk(root_path)

def save_tree(tree, out_path):
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(tree, f, indent=2)
