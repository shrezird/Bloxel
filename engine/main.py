import atexit

from runtime.services.utilities import p, local_directory
from runtime.services.log import start_logging, set_log_directory, stop_logging
from runtime.services.directory import verify_local_directory
from runtime.services.window import window

p("ENGINE: main.py started")

def start_engine():
    log = start_logging()
    verify_local_directory()
    set_log_directory(local_directory())
    atexit.register(stop_logging)
    return log

def main():
    start_engine()
    window()

main()

p("ENGINE: main.py stopped")