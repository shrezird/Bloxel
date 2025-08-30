import os

from runtime.services.backend.utilities import p, local_directory

def configuration():
    return os.path.join(local_directory(), "configuration.json")

#class engine:
# TODO: window_state_load, window_state_save; Only three state types will be saved/loaded: fullscreen, maximized, and resized.

def start_service_configuration():
    p("SERVICES: configuration.py started")

def stop_service_configuration():
    p("SERVICES: configuration.py stopping")