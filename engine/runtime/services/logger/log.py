import os, datetime, json, atexit, sys

class DualOutput:
    def __init__(self, original, log_file):
        self.original = original
        self.log_file = log_file

    def write(self, text):
        self.original.write(text)
        self.log_file.write(text)

    def flush(self):
        self.original.flush()
        self.log_file.flush()

start_time = None
file_path = None
original_stdout = None
log_file = None

def get_timestamp():
    return datetime.datetime.now().strftime('[%H:%M:%S]')

def get_log_directory():
    return os.path.join(os.getenv('LOCALAPPDATA') or os.path.expanduser('~\\AppData\\Local'), 'Bloxel', 'logs')

def log():
    global start_time, file_path, original_stdout, log_file
    version_file = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'version.json')
    with open(version_file) as f:
        version = json.load(f)['version']
    now = datetime.datetime.now()
    date = now.strftime('%m.%d.%y')
    time_str = now.strftime('%H.%M.%S.%f')
    file_name = f'{version} {date} {time_str}.txt'
    log_dir = get_log_directory()
    os.makedirs(log_dir, exist_ok=True)
    file_path = os.path.join(log_dir, file_name)
    start_time = now
    with open(file_path, 'w') as f:
        f.write(f'Engine: {version}\n')
        f.write(f'Start: {now.strftime('%m/%d/%Y')} - {now.strftime('%H:%M:%S:%f')}\n')
        f.write('\n\n\n')
    original_stdout = sys.stdout
    log_file = open(file_path, 'a', buffering=1)
    sys.stdout = DualOutput(original_stdout, log_file)
    atexit.register(close_log)
    print(f'{get_timestamp()} SERVICE: log.py has been initialized, created new log at {log_dir}')

def close_log():
    global start_time, file_path, original_stdout, log_file
    if file_path and start_time:
        end_time = datetime.datetime.now()
        total_seconds = (end_time - start_time).total_seconds()
        hours, remainder = divmod(int(total_seconds), 3600)
        minutes, seconds = divmod(remainder, 60)
        log_file.write(f'{get_timestamp()} SERVICE: log.py has been stopped, saved log at {get_log_directory()}\n')
        log_file.write('\n\n\n')
        log_file.write(f'End: {end_time.strftime('%m/%d/%Y')} - {end_time.strftime('%H:%M:%S:%f')}\n')
        log_file.write(f'Total Playtime: {hours:02d}:{minutes:02d}:{seconds:02d}\n')
        sys.stdout = original_stdout
        print(f'{get_timestamp()} SERVICE: log.py has been stopped, saved log at {get_log_directory()}')
        log_file.close()

def time():
    return get_timestamp()

def log_directory():
    return get_log_directory()