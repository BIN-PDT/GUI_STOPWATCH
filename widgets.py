import customtkinter as ctk
from settings import *


class ControlFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(master=parent, fg_color="transparent", corner_radius=0)
        self.grid(row=1, column=0, sticky=ctk.NSEW, padx=5, pady=5)
        # LAYOUT.
        self.rowconfigure(0, weight=1, uniform="A")
        self.columnconfigure(0, weight=1, uniform="A")
        self.columnconfigure(1, weight=9, uniform="A")
        self.columnconfigure(2, weight=1, uniform="A")
        self.columnconfigure(3, weight=9, uniform="A")
        self.columnconfigure(4, weight=1, uniform="A")
        # DATA.
        font = (FONT, BUTTON_FONT_SIZE)
        # WIDGET.
        self.lap_button = ctk.CTkButton(
            master=self,
            fg_color=GREY,
            text="LAP",
            font=font,
            state=ctk.DISABLED,
            command=self.handle_lap,
        )
        self.run_button = ctk.CTkButton(
            master=self,
            fg_color=GREEN,
            hover_color=GREEN_HIGHLIGHT,
            text="START",
            font=font,
            text_color=GREEN_TEXT,
            command=self.handle_run,
        )
        self.lap_button.grid(row=0, column=1, sticky=ctk.NSEW)
        self.run_button.grid(row=0, column=3, sticky=ctk.NSEW)

    def handle_lap(self):
        pass

    def handle_run(self):
        pass
