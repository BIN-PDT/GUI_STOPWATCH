import customtkinter as ctk
from settings import *


class App(ctk.CTk):
    def __init__(self):
        super().__init__(fg_color=BLACK)
        # SETUP.
        ctk.set_appearance_mode("dark")
        self.geometry("300x600")
        self.resizable(False, False)
        self.iconbitmap("images/empty.ico")
        self.title("")


if __name__ == "__main__":
    App().mainloop()
