import os, datetime

def time():
    return datetime.datetime.now().strftime("[%H:%M:%S]")

def log_directory():
    return os.path.join(os.getenv('LOCALAPPDATA') or os.path.expanduser('~\\AppData\\Local'), 'Bloxel', 'logs')

def log():
    print(f"{time()} SERVICE: log.py has been initialized, creating new log at {log_directory()}")