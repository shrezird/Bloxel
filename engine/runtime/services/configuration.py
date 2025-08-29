import os

from runtime.services.utilities import p, local_directory

def configuration():
    return os.path.join(local_directory(), "configuration.json")

# !PLACEHOLDER!
def load_window_state():
    p(f"SERVICES: configuration.py loaded window state = {configuration()}")

def save_window_state():
    p(f"SERVICES: configuration.py saved window state = {configuration()}")

def start_service_configuration():
    p("SERVICES: configuration.py started")

def stop_service_configuration():
    p("SERVICES: configuration.py stopping")