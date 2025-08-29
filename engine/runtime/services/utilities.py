import time, os

def test():
    return os

def p(string):
    print(f"{time.strftime("[%H:%M:%S]")} {string}")

def local_directory():
    return os.path.join(os.getenv("LOCALAPPDATA") or os.path.expanduser("~\\AppData\\Local"), "Bloxel")

def start_service_utilities():
    p("SERVICES: utilities.py started")

def stop_service_utilities():
    p("SERVICES: utilities.py stopping")