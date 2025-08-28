import atexit
from runtime.services.directory import verify_directory, get_local_directory
from runtime.services.log import initialize_logging, set_log_directory, stop_logging, get_timestamp
from runtime.services.window import window

def setup_engine():
    log_manager = initialize_logging()
    print(f'{get_timestamp()} ENGINE: main.py is setting up the engine')
    verify_directory()
    set_log_directory(get_local_directory())
    atexit.register(stop_logging)
    return log_manager

def main():
    setup_engine()
    print(f'{get_timestamp()} ENGINE: main.py has set up the engine, launching window...')
    window()

main()
print(f'{get_timestamp()} ENGINE: main.py has been stopped')