import json, webview
from pathlib import Path

def window():
    build = json.load(open(Path(__file__).parent.parent / 'configuration.json'))['build']
    url = (Path(__file__).parent.parent / 'game' / 'index.html').resolve().as_uri()

    class Api:
        def __init__(self):
            self.window = None
            self.fullscreen = False
            self.maximized = True
        def f11(self):
            self.window.toggle_fullscreen()
            self.fullscreen = not self.fullscreen
            if not self.fullscreen:
                self.window.maximize()
        def on_window_restore(self):
            if self.maximized:
                self.window.resize(960, 540)
            self.maximized = False
        def on_window_maximize(self):
            self.maximized = True
    api = Api()
    window = webview.create_window(
        f'Bloxel - {build}',
        url,
        width = 960,
        height = 540,
        min_size = (960, 540),
        js_api = api
    )
    api.window = window
    def on_loaded():
        window.evaluate_js("""
            document.addEventListener('keydown', function(e){
                if(e.key==='F11'){ e.preventDefault(); pywebview.api.f11(); }
            });
        """)
    
    def on_window_restored():
        api.on_window_restore()
    
    def on_window_maximized():
        api.on_window_maximize()
    
    window.events.loaded += on_loaded
    window.events.restored += on_window_restored
    window.events.maximized += on_window_maximized
    webview.start(window.maximize)

window()

# TODO: Implement local storage directory creation and loading.