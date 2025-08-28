import time, os

def p(string):
    print(f"{time.strftime("[%H:%M:%S]")} {string}")

def local_directory():
    return os.path.join(os.getenv("LOCALAPPDATA") or os.path.expanduser("~\\AppData\\Local"), "Bloxel")

p("SERVICES: utilities.py started")