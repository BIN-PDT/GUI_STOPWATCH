import customtkinter as ctk
from settings import *
from widgets import *


class App(ctk.CTk):
    def __init__(self):
        super().__init__(fg_color=BLACK)
        # SETUP.
        ctk.set_appearance_mode("dark")
        self.geometry("300x600")
        self.resizable(False, False)
        self.iconbitmap("images/empty.ico")
        self.title("")
        # LAYOUT.
        self.rowconfigure(0, weight=5, uniform="A")
        self.rowconfigure(1, weight=1, uniform="A")
        self.rowconfigure(2, weight=4, uniform="A")
        self.columnconfigure(0, weight=1, uniform="A")
        # WIDGET.
        self.control_frame = ControlFrame(
            self, self.start, self.pause, self.resume, self.reset, self.lap
        )

    def start(self):
        print(self.start.__name__)

    def pause(self):
        print(self.pause.__name__)

    def resume(self):
        print(self.resume.__name__)

    def reset(self):
        print(self.reset.__name__)

    def lap(self):
        print(self.lap.__name__)


if __name__ == "__main__":
    App().mainloop()
