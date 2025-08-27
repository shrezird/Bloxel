import os

def local_directory():
    return os.path.join(os.getenv('LOCALAPPDATA') or os.path.expanduser('~\\AppData\\Local'), 'Bloxel')

def directory_verify():
    directory = local_directory()
    if not os.path.isdir(directory):
        directory_create()

def directory_create():
    directory = local_directory()
    os.makedirs(directory, exist_ok=True)
    os.makedirs(os.path.join(directory, 'logs'), exist_ok=True)

    config_path = os.path.join(directory, 'configuration.json')
    if not os.path.isfile(config_path):
        with open(config_path, 'w', encoding='utf-8') as f:
            f.write('{}')