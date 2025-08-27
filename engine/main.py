import webview
from runtime.services.directory import directory_verify
from runtime.services.log import log

directory_verify()
log()

webview.create_window(
    title = 'Bloxel',
    url = 'runtime/index.html'
)
webview.start()