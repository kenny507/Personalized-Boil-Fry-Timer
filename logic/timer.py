import time
import threading
import winsound
import os,sys


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


class Timer:
    def __init__(self, update_callback, done_callback):
        self.time_left = 0
        self.running = False
        self.thread = None
        self.stop_event = threading.Event()
        self.update_callback = update_callback
        self.done_callback = done_callback

    def start(self, duration):
        if self.running:
            return
        self.time_left = duration
        self.running = True
        self.stop_event.clear()
        self.thread = threading.Thread(target=self._run)
        self.thread.daemon = True
        self.thread.start()

    def stop(self):
        if not self.running:
            return
        self.stop_event.set()
        self.running = False

    def _run(self):
        try:
            while self.time_left > 0 and not self.stop_event.is_set():
                mins, secs = divmod(self.time_left, 60)
                self.update_callback(f"{mins:02}:{secs:02}")
                time.sleep(1)
                self.time_left -= 1
        except Exception as e:
            print(f"Error in timer thread: {e}")
        finally:
            self.running = False

    def _ring(self):
        try:
            sound_path = resource_path("assets/timer_complete_music.wav")
            winsound.PlaySound(sound_path, winsound.SND_FILENAME | winsound.SND_ASYNC)
        except Exception as e:
            print(f"Failed to play sound: {e}")

