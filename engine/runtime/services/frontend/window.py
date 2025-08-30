import webview, keyboard

from runtime.services.backend.utilities import p
from runtime.services.backend.log import get_logger

def start_window():
    window = webview.create_window(
        title="Bloxel",
        url="runtime/index.html",
        min_size=(515, 360),
        width=515,
        height=360,
        maximized=True,
        js_api=get_logger()
    )

    fullscreened = False
    maximized = True

    def fullscreen():
        nonlocal fullscreened
        nonlocal maximized
        if fullscreened == False:
            fullscreened = True
            maximized = False
            window.resize(515, 360)
            window.toggle_fullscreen()
        else:
            fullscreened = False
            maximized = True
            window.toggle_fullscreen()
            window.maximize()
        p(f"SERVICES: window.py fullscreen = {fullscreened}")
        p(f"SERVICES: window.py maximized = {maximized}")

    def hotkey_fullscreen():
        keyboard.add_hotkey('f11', fullscreen)

    webview.start(hotkey_fullscreen)

def start_service_window():
    p("SERVICES: window.py started")

def stop_service_window():
    p("SERVICES: window.py stopping")