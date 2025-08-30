import webview
import keyboard

from runtime.services.backend.utilities import p
from runtime.services.backend.log import get_logger

def start_window():
    main = webview.create_window(
        title="Bloxel",
        url="runtime/index.html",
        maximized=True,
        min_size=(515, 360),
        js_api=get_logger()
    )

    def minimize():
        p("SERVICES: window.py minimized")

    def restore():
        p("SERVICES: window.py restored")

    main.events.minimized += minimize
    main.events.restored += restore

    def fullscreen():
        if main.fullscreen:
            main.toggle_fullscreen()
            main.maximized = True
        else:
            main.toggle_fullscreen()
            main.maximized = False

    def hotkey_fullscreen():
        keyboard.add_hotkey('f11', fullscreen)

    webview.start(hotkey_fullscreen)

def start_service_window():
    p("SERVICES: window.py started")

def stop_service_window():
    p("SERVICES: window.py stopping")