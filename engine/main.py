import webview
from runtime.loader.load import load

webview.create_window(
    title = 'Bloxel',
    url = load.index,
)

webview.start()