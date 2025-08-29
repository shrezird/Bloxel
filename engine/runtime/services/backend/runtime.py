from runtime.services.backend.utilities import p, start_service_utilities, stop_service_utilities
from runtime.services.backend.log import start_service_log, stop_service_log
from runtime.services.backend.directory import start_service_directory
from runtime.services.frontend.window import start_service_window, stop_service_window
from runtime.services.backend.configuration import start_service_configuration, stop_service_configuration

def start_runtime():
    from main import start_engine_main
    start_engine_main()
    start_service_runtime()
    start_service_utilities()
    start_service_log()
    start_service_directory()
    start_service_window()
    start_service_configuration()

def stop_runtime():
    from main import stop_engine_main
    stop_service_window()
    stop_service_configuration()
    stop_service_log()
    stop_service_utilities()
    stop_service_runtime()
    stop_engine_main()

def start_service_runtime():
    p("SERVICES: runtime.py started")

def stop_service_runtime():
    p("SERVICES: runtime.py stopping")