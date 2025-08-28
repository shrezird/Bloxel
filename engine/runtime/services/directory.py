import os
from runtime.services.log import get_timestamp

def get_local_directory():
    return os.path.join(os.getenv('LOCALAPPDATA') or os.path.expanduser('~\\AppData\\Local'), 'Bloxel')

def verify_directory():
    print(f'{get_timestamp()} SERVICE: directory.py has been initialized')
    directory = get_local_directory()
    if os.path.isdir(directory):
        print(f'{get_timestamp()} SERVICE: directory.py has found {directory}')
        print(f'{get_timestamp()} SERVICE: directory.py has been stopped')
    else:
        print(f'{get_timestamp()} SERVICE: directory.py could not find {directory}, attempting to create the necessary directories...')
        create_directory()

def create_directory():
    directory = get_local_directory()
    os.makedirs(directory, exist_ok=True)
    print(f'{get_timestamp()} SERVICE: directory.py has created {directory}')
    os.makedirs(os.path.join(directory, 'logs'), exist_ok=True)
    print(f'{get_timestamp()} SERVICE: directory.py has created {os.path.join(directory, "logs")}')
    open(os.path.join(directory, 'configuration.json'), 'a').close()
    print(f'{get_timestamp()} SERVICE: directory.py has created {os.path.join(directory, "configuration.json")}')
    print(f'{get_timestamp()} SERVICE: directory.py has finished creating {directory}')
    print(f'{get_timestamp()} SERVICE: directory.py has been stopped')