import webview

from runtime.services.backend.configuration import load_window_state, save_window_state
from runtime.services.backend.log import get_logger
from runtime.services.backend.utilities import p

load_window_state()
save_window_state()

def window():
    webview.create_window(
        title="Bloxel",
        url="runtime/index.html",
        min_size=(960, 540),
        js_api=get_logger()
    )

    webview.start()

def start_service_window():
    p("SERVICES: window.py started")

def stop_service_window():
    p("SERVICES: window.py stopping")