import os

from runtime.services.utilities import p, local_directory

p("SERVICES: directory.py started")

def verify_local_directory():
    if os.path.isdir(local_directory()):
        p(f"SERVICES: directory.py found = {local_directory()}")
        p(f"SERVICES: directory.py stopped (code 0)")
    else:
        p(f"SERVICES: directory.py could not find {local_directory()}, creating the necessary directories...")
        create_local_directory()

def create_local_directory():
    os.makedirs(local_directory(), exist_ok=True)
    p(f"SERVICES: directory.py created = {local_directory()}")

    os.makedirs(os.path.join(local_directory(), "logs"), exist_ok=True)
    p(f"SERVICES: directory.py created = {os.path.join(local_directory(), "logs")}")

    p(f"SERVICES: directory.py finished creating = {local_directory()}")
    p(f"SERVICES: directory.py stopped (code 1)")