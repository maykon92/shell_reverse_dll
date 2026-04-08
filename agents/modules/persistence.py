import os

def set_persistence():
    path = os.path.expanduser("~/.config/startup")
    with open(path, "w") as f:
        f.write("python3 /path/to/agent.py &")
    os.chmod(path, 0o755)