import webview
import keyboard

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

    def maximized():
        if window.maximized == True:
            p(f"SERVICES: window.py maximized = True")
        else:
            p(f"SERVICES: window.py maximized = False")

    def resized():
        width = window.width
        height = window.height
        p(f"SERVICES: window.py resized = {width}x{height}")

    window.events.resized += resized

    fullscreened = False
    
    def fullscreen():
        nonlocal fullscreened
        if fullscreened == False:
            fullscreened = True
            window.resize(515, 360)
            window.toggle_fullscreen()
            p(f"SERVICES: window.py fullscreen = True")
            maximized()
        else:
            fullscreened = False
            window.toggle_fullscreen()
            window.maximize()
            p(f"SERVICES: window.py fullscreen = False")
            maximized()

    def hotkey_fullscreen():
        keyboard.add_hotkey('f11', fullscreen)

    webview.start(hotkey_fullscreen)

def start_service_window():
    p("SERVICES: window.py started")

def stop_service_window():
    p("SERVICES: window.py stopping")