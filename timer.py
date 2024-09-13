from time import time


class Timer:
    def __init__(self):
        self.start_time = None
        self.pause_time = None
        self.is_paused = False

    def get(self):
        return int(round(time() - self.start_time, 2) * 1000)

    def start(self):
        self.start_time = time()

    def pause(self):
        self.pause_time = time()
        self.is_paused = True

    def resume(self):
        elapsed_time = time() - self.pause_time
        self.start_time += elapsed_time
        self.pause_time = None
        self.is_paused = False

    def reset(self):
        self.start_time = None
        self.pause_time = None
        self.is_paused = False
