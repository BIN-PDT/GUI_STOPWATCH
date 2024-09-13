import customtkinter as ctk
from settings import *
from widgets import *
from timer import Timer


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
        # DATA.
        self.timer = Timer()
        self.is_active = False
        # WIDGET.
        self.clock = Clock(self)
        self.control_frame = ControlFrame(
            self, self.start, self.pause, self.resume, self.reset, self.lap
        )

    def animate(self):
        if self.is_active:
            self.clock.draw(self.timer.get())
            self.after(FRAMERATE, self.animate)

    def start(self):
        self.is_active = True
        self.timer.start()
        self.animate()

    def pause(self):
        self.is_active = False
        self.timer.pause()

    def resume(self):
        self.is_active = True
        self.timer.resume()
        self.animate()

    def reset(self):
        self.timer.reset()
        self.clock.draw()

    def lap(self):
        print(self.timer.get())


if __name__ == "__main__":
    App().mainloop()
