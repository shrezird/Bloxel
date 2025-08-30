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

    last_window_state = "maximized"
    def maximize():
        nonlocal last_window_state
        if last_window_state != "maximized":
            p("SERVICES: window.py maximized")
        last_window_state = "maximized"
    def unmaximize():
        nonlocal last_window_state
        if last_window_state == "maximized" and not window.fullscreen:
            window.resize(515, 360)
            p("SERVICES: window.py unmaximized")
        last_window_state = "unmaximized"

    window.events.maximized += maximize
    window.events.restored += unmaximize

    is_fullscreen = False
    def fullscreen():
        nonlocal is_fullscreen
        fullscreened = not is_fullscreen
        is_fullscreen = not is_fullscreen
        window.toggle_fullscreen()
        if fullscreened:
            p("SERVICES: window.py fullscreened")
        else:
            window.maximize()
            p("SERVICES: window.py maximized")

    def hotkey_fullscreen():
        keyboard.add_hotkey('f11', fullscreen)

    webview.start(hotkey_fullscreen)

def start_service_window():
    p("SERVICES: window.py started")

def stop_service_window():
    p("SERVICES: window.py stopping")