import customtkinter as ctk
from settings import *


class ControlFrame(ctk.CTkFrame):
    def __init__(self, parent, start, pause, resume, reset, lap):
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
        self.start, self.pause, self.resume = start, pause, resume
        self.reset, self.lap = reset, lap
        self.state = "OFF"
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
        if self.state == "ON":
            self.lap()
        else:
            self.reset()
            self.state = "OFF"

        self.update_buttons()

    def handle_run(self):
        match self.state:
            case "OFF":
                self.state = "ON"
                self.start()
            case "ON":
                self.state = "PAUSE"
                self.pause()
            case "PAUSE":
                self.state = "ON"
                self.resume()

        self.update_buttons()

    def update_buttons(self):
        match self.state:
            case "OFF":
                self.lap_button.configure(
                    fg_color=GREY,
                    text="LAP",
                    state=ctk.DISABLED,
                )

                self.run_button.configure(text="START")
            case "ON":
                self.lap_button.configure(
                    fg_color=ORANGE_DARK,
                    hover_color=ORANGE_HIGHLIGHT,
                    text="LAP",
                    text_color=ORANGE_DARK_TEXT,
                    state=ctk.NORMAL,
                )

                self.run_button.configure(
                    fg_color=RED,
                    hover_color=RED_HIGHLIGHT,
                    text="STOP",
                    text_color=RED_TEXT,
                )
            case "PAUSE":
                self.lap_button.configure(text="RESET")

                self.run_button.configure(
                    fg_color=GREEN,
                    hover_color=GREEN_HIGHLIGHT,
                    text="RESUME",
                    text_color=GREEN_TEXT,
                )
