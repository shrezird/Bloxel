from runtime.services import runtime
from runtime.services.utilities import p, local_directory
from runtime.services.log import start_logging, set_log_directory, stop_logging
from runtime.services.directory import verify_local_directory
from runtime.services.window import window

def start_engine():
    log = start_logging()
    runtime.start()
    verify_local_directory()
    set_log_directory(local_directory())
    return log

def stop_engine():
    runtime.stop()
    stop_logging()

def start_main():
    start_engine()
    window()

def start_engine_main():
    p("ENGINE: main.py started")

def stop_engine_main():
    p("ENGINE: main.py stopping")

if __name__ == "__main__":
    start_main()
    stop_engine()