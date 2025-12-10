import re, os

def get_identifiers(file_path, lang="python"):
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            code = f.read()
    except Exception:
        return {"functions": [], "classes": []}
    funcs = re.findall(r'^\s*def\s+([A-Za-z_][A-Za-z0-9_]*)', code, re.M)
    classes = re.findall(r'^\s*class\s+([A-Za-z_][A-Za-z0-9_]*)', code, re.M)
    return {"functions": funcs, "classes": classes}

def read_readme(repo_path):
    candidates = ["README.md", "readme.md", "README.MD"]
    for c in candidates:
        p = os.path.join(repo_path, c)
        if os.path.exists(p):
            try:
                with open(p, "r", encoding="utf-8") as f:
                    return f.read()
            except Exception:
                return ""
    return ""
