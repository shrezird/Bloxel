import webview
from runtime.services.log import get_timestamp
from runtime.services.log import get_logger

def window():
    webview.create_window(
        title='Bloxel',
        url='runtime/index.html',
        js_api=get_logger()
    )
    print(f'{get_timestamp()} SERVICE: window.py has been initialized')
    webview.start()