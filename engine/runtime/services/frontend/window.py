import webview
import keyboard

from runtime.services.backend.utilities import p
from runtime.services.backend.log import get_logger

def start_window():
    window = webview.create_window(
        title="Bloxel",
        url="runtime/index.html",
        maximized=True,
        min_size=(515, 360),
        js_api=get_logger()
    )
    
    is_fullscreen = False

    def fullscreen():
        nonlocal is_fullscreen
        is_fullscreen = not is_fullscreen
        window.toggle_fullscreen()
        p(f"SERVICES: window.py fullscreen = {is_fullscreen}")
        if not is_fullscreen:
            window.maximize()

    def hotkey_fullscreen():
        keyboard.add_hotkey('f11', fullscreen)

    webview.start(hotkey_fullscreen)

def start_service_window():
    p("SERVICES: window.py started")

def stop_service_window():
    p("SERVICES: window.py stopping")