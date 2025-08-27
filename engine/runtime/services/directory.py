import os, datetime

def time():
    return datetime.datetime.now().strftime("[%H:%M:%S]")

def local_directory():
    return os.path.join(os.getenv('LOCALAPPDATA') or os.path.expanduser('~\\AppData\\Local'), 'Bloxel')

def directory_verify():
    directory = local_directory()
    if os.path.isdir(directory):
        print(f"{time()} SERVICE: directory.py has verified local directory at {directory}")
    else:
        print(f"{time()} SERVICE: directory.py could not verify local directory")
        directory_create()

def directory_create():
    directory = local_directory()
    os.makedirs(directory, exist_ok=True)
    os.makedirs(os.path.join(directory, 'logs'), exist_ok=True)

    config_path = os.path.join(directory, 'configuration.json')
    if not os.path.isfile(config_path):
        with open(config_path, 'w', encoding='utf-8') as f:
            f.write('{}')

    print(f"{time()} SERVICE: directory.py has created a new local directory at {directory}")