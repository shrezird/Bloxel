import webview

from runtime.services.backend.utilities import p
from runtime.services.backend.log import get_logger

def window():
    webview.create_window(
        title="Bloxel",
        url="runtime/index.html",
        maximized=True,
        min_size=(515, 360),
        js_api=get_logger()
    )

    webview.start()

def start_service_window():
    p("SERVICES: window.py started")

def stop_service_window():
    p("SERVICES: window.py stopping")