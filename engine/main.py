import webview, atexit, datetime
from runtime.services.directory import verify_directory, get_local_directory
from runtime.services.log import get_logger, initialize_logging, set_log_directory, stop_logging

def get_timestamp():
    return datetime.datetime.now().strftime('[%H:%M:%S]')

log_manager = initialize_logging()

verify_directory()

set_log_directory(get_local_directory())

atexit.register(stop_logging)

window = webview.create_window(
    title='Bloxel',
    url='runtime/index.html',
    js_api=get_logger()
)

webview.start()
print(f'{get_timestamp()} ENGINE: Engine has exited by request of user')