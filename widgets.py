from math import sin, cos, radians
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


class Clock(ctk.CTkCanvas):
    def __init__(self, parent):
        super().__init__(
            master=parent,
            background=BLACK,
            bd=0,
            highlightthickness=0,
            relief=ctk.RIDGE,
        )
        self.grid(row=0, column=0, sticky=ctk.NSEW, padx=5, pady=5)
        # SETUP.
        self.bind("<Configure>", self.load_data)

    def load_data(self, event):
        self.SIZE = event.width, event.height

        RADIUS = event.width / 2
        self.CENTER = RADIUS, RADIUS
        self.OUT_RADIUS = RADIUS * 0.95
        self.INN_RADIUS = RADIUS * 0.85
        self.MID_RADIUS = RADIUS * 0.9
        self.NUM_RADIUS = RADIUS * 0.7
        self.CEN_RADIUS = RADIUS * 0.2

        self.draw()

    def draw(self, milliseconds=0):
        self.draw_border()
        self.draw_center()

    def draw_center(self):
        self.create_oval(
            self.CENTER[0] - CENTER_GAP,
            self.CENTER[1] - CENTER_GAP,
            self.CENTER[0] + CENTER_GAP,
            self.CENTER[1] + CENTER_GAP,
            fill=BLACK,
            outline=ORANGE,
            width=LINE_WIDTH,
        )

    def draw_border(self):
        for angle in range(360):
            sin_alpha = sin(radians(angle - 90))
            cos_alpha = cos(radians(angle - 90))

            outer_x = self.CENTER[0] + self.OUT_RADIUS * cos_alpha
            outer_y = self.CENTER[1] + self.OUT_RADIUS * sin_alpha
            if angle % 30 == 0:
                inner_x = self.CENTER[0] + self.INN_RADIUS * cos_alpha
                inner_y = self.CENTER[1] + self.INN_RADIUS * sin_alpha
                self.create_line(
                    (outer_x, outer_y),
                    (inner_x, inner_y),
                    fill=WHITE,
                    width=LINE_WIDTH,
                )
            elif angle % 6 == 0:
                middle_x = self.CENTER[0] + self.MID_RADIUS * cos_alpha
                middle_y = self.CENTER[1] + self.MID_RADIUS * sin_alpha
                self.create_line(
                    (outer_x, outer_y),
                    (middle_x, middle_y),
                    fill=GREY,
                    width=LINE_WIDTH,
                )
