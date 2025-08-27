import webview
from datetime import datetime
from runtime.services.directory import directory_verify
from runtime.services.logger.log import log

class ConsoleAPI:
    def print_console(self, msg):
        current_time = datetime.now().strftime("%H:%M:%S")
        print(f"[{current_time}] {msg}")

directory_verify()
log()

api = ConsoleAPI()

window = webview.create_window(
    title = 'Bloxel',
    url = 'runtime/index.html',
    js_api=api
)

def on_loaded():
    pass

window.events.loaded += on_loaded

webview.start()