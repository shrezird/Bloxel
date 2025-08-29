from runtime.services.backend.runtime import start_runtime, stop_runtime
from runtime.services.backend.utilities import p, local_directory
from runtime.services.backend.log import start_logging, set_log_directory, stop_logging
from runtime.services.backend.directory import verify_local_directory
from runtime.services.frontend.window import window

def start_engine():
    log = start_logging()
    start_runtime()
    verify_local_directory()
    set_log_directory(local_directory())
    return log

def stop_engine():
    stop_runtime()
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