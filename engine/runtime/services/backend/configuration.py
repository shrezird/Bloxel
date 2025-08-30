import os

from runtime.services.backend.utilities import p, local_directory

def configuration():
    return os.path.join(local_directory(), "configuration.json")

# !This is a placeholder for future engine configuration settings!
class engine:
    class settings:
        pass

# runtime.py accesses for logging runtime start/stop events.
def start_service_configuration():
    p("SERVICES: configuration.py started")

def stop_service_configuration():
    p("SERVICES: configuration.py stopping")