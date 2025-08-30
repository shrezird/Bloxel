import time, os

def p(string):
    print(f"{time.strftime("[%H:%M:%S]")} {string}")

def local_directory():
    return os.path.join(os.getenv("LOCALAPPDATA") or os.path.expanduser("~\\AppData\\Local"), "Bloxel")

# runtime.py accesses for logging runtime start/stop events.
def start_service_utilities():
    p("SERVICES: utilities.py started")

def stop_service_utilities():
    p("SERVICES: utilities.py stopping")