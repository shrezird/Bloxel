import datetime, sys, threading, json, os, queue, time

from runtime.services.utilities import p

def get_detailed_timestamp():
    return datetime.datetime.now().strftime("%m/%d/%y - %H:%M:%S:%f")[:-4]

def get_filename_timestamp():
    return datetime.datetime.now().strftime("%m.%d.%y - %H.%M.%S.%f")[:-4]

class log_capture:
    def __init__(self, log_manager_instance, original_stream):
        self.log_manager_instance = log_manager_instance
        self.original_stream = original_stream

    def write(self, text):
        self.original_stream.write(text)
        if text.strip():
            self.log_manager_instance.log_message(text.strip())

    def flush(self):
        self.original_stream.flush()

class log_manager:
    def __init__(self):
        self.log_file_path = None
        self.cached_messages = []
        self.start_time = datetime.datetime.now()
        self.log_directory = None
        self.version = self.load_version()
        self.playtime_thread = None
        self.running = True
        self.original_stdout = sys.stdout
        self.original_stderr = sys.stderr
        self.message_queue = queue.Queue()
        self.log_writer_thread = None
        self.log_lock = threading.Lock()
        self.start_log_writer()
        sys.stdout = log_capture(self, self.original_stdout)
        sys.stderr = log_capture(self, self.original_stderr)
        p("SERVICES: log.py started")

    def load_version(self):
        with open("version.json", "r") as file:
            return json.load(file)["version"]

    def set_log_directory(self, directory):
        self.log_directory = os.path.join(directory, "logs")
        if os.path.exists(self.log_directory):
            self.create_log()
            self.flush_cached_messages()
            p(f"SERVICES: log.py created log = {self.log_file_path}")

    def create_log(self):
        if not self.log_directory:
            return
        self.cleanup_old_logs()
        filename = f"{self.version} - {get_filename_timestamp()}.txt"
        self.log_file_path = os.path.join(self.log_directory, filename)
        start_time = get_detailed_timestamp()
        initial_content = (
            f"Engine: {self.version}\n"
            f"Total Playtime: 0:0:0:0\n"
            f"\nStart: {start_time}\n\n"
        )
        with open(self.log_file_path, "w") as file:
            file.write(initial_content)
        self.start_playtime_tracking()

    def cleanup_old_logs(self):
        if not self.log_directory or not os.path.exists(self.log_directory):
            return
        log_files = [file for file in os.listdir(self.log_directory) if file.endswith(".txt")]
        if len(log_files) >= 50:
            log_files.sort(key=lambda file: os.path.getctime(os.path.join(self.log_directory, file)))
            for log_file in log_files[:-49]:
                old_log_path = os.path.join(self.log_directory, log_file)
                os.remove(old_log_path)
                p(f"SERVICES: log.py removed = {log_file}")

    def flush_cached_messages(self):
        if self.cached_messages and self.log_file_path:
            for message in self.cached_messages:
                self.write_message_to_log(message)
            self.cached_messages.clear()

    def start_log_writer(self):
        self.log_writer_thread = threading.Thread(target=self.process_log_messages, daemon=True)
        self.log_writer_thread.start()

    def process_log_messages(self):
        while self.running:
            try:
                message = self.message_queue.get(timeout=0.1)
                if message is None:
                    break
                self.write_message_to_log(message)
                self.message_queue.task_done()
            except queue.Empty:
                continue

    def write_message_to_log(self, message):
        with self.log_lock:
            if self.log_file_path and os.path.exists(self.log_file_path):
                try:
                    with open(self.log_file_path, "r", encoding="utf-8") as file:
                        content = file.read()
                    lines = content.split("\n")
                    insert_index = len(lines)
                    for index, line in enumerate(lines):
                        if line.startswith("End:"):
                            insert_index = index
                            break
                    if insert_index == len(lines):
                        for index in range(len(lines) - 1, -1, -1):
                            if lines[index].strip():
                                insert_index = index + 1
                                break
                    lines.insert(insert_index, message)
                    with open(self.log_file_path, "w", encoding="utf-8") as file:
                        file.write("\n".join(lines))
                except Exception:
                    self.cached_messages.append(message)

    def start_playtime_tracking(self):
        if self.playtime_thread and self.playtime_thread.is_alive():
            return
        self.playtime_thread = threading.Thread(target=self.update_playtime, daemon=True)
        self.playtime_thread.start()

    def update_playtime(self):
        while self.running and self.log_file_path:
            try:
                with self.log_lock:
                    elapsed = datetime.datetime.now() - self.start_time
                    hours, remainder = divmod(elapsed.total_seconds(), 3600)
                    minutes, seconds = divmod(remainder, 60)
                    milliseconds = elapsed.microseconds // 1000
                    playtime_str = f"{int(hours)}:{int(minutes)}:{int(seconds)}:{milliseconds}"
                    with open(self.log_file_path, "r", encoding="utf-8") as file:
                        content = file.read()
                    lines = content.split("\n")
                    for index, line in enumerate(lines):
                        if line.startswith("Total Playtime:"):
                            lines[index] = f"Total Playtime: {playtime_str}"
                            break
                    with open(self.log_file_path, "w", encoding="utf-8") as file:
                        file.write("\n".join(lines))
                time.sleep(0.1)
            except Exception:
                break

    def log_message(self, message):
        if self.log_file_path:
            self.message_queue.put(message)
        else:
            self.cached_messages.append(message)

    def stop(self):
        p("SERVICES: log.py stopped")
        self.running = False
        self.message_queue.put(None)
        if self.log_writer_thread:
            self.log_writer_thread.join(timeout=1.0)
        if self.log_file_path and os.path.exists(self.log_file_path):
            with self.log_lock:
                with open(self.log_file_path, "r", encoding="utf-8") as file:
                    content = file.read()
                end_time = get_detailed_timestamp()
                if not content.endswith("\n\n"):
                    if content.endswith("\n"):
                        content += "\n"
                    else:
                        content += "\n\n"
                content += f"End: {end_time}"
                with open(self.log_file_path, "w", encoding="utf-8") as file:
                    file.write(content)
            p(f"SERVICES: log.py saved log = {self.log_file_path}")
        sys.stdout = self.original_stdout
        sys.stderr = self.original_stderr

log_manager_instance = None
webview_connected = False

def start_logging():
    global log_manager_instance
    if log_manager_instance is None:
        log_manager_instance = log_manager()
    return log_manager_instance

def set_log_directory(directory):
    global log_manager_instance
    if log_manager_instance:
        log_manager_instance.set_log_directory(directory)

def stop_logging():
    global log_manager_instance
    if log_manager_instance:
        log_manager_instance.stop()

class webview_logger:
    def print_console(self, message):
        global webview_connected
        if not webview_connected:
            p("SERVICES: log.py is logging index.html")
            webview_connected = True
        p(f"{message}")

def get_logger():
    return webview_logger()