import os

from runtime.services.backend.utilities import p, local_directory

def configuration():
    return os.path.join(local_directory(), "configuration.json")

#class engine:

def start_service_configuration():
    p("SERVICES: configuration.py started")

def stop_service_configuration():
    p("SERVICES: configuration.py stopping")