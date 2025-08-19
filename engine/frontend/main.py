import json, webview
from pathlib import Path

def window():
    build = json.load(open(Path(__file__).parent.parent / 'configuration.json'))['build']
    url = (Path(__file__).parent.parent / 'game' / 'index.html').resolve().as_uri()

    window = webview.create_window(
        f'Bloxel - {build}',
        url,
        width = 960,
        height = 540,
        min_size = (960, 540)
    )
    webview.start(window.maximize)

window()

# TODO: Implement Discord Rich Presence & F11 for fullscreen.