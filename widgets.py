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
        self.bind("<Configure>", self.on_load)

    def on_load(self, event):
        RADIUS = event.width / 2
        self.CENTER = RADIUS, RADIUS
        # FOR DRAWING MARK.
        self.OUT_RADIUS = RADIUS * 0.95
        self.MID_RADIUS = RADIUS * 0.90
        self.INN_RADIUS = RADIUS * 0.85
        # FOR DRAWING NUMBER & HANDLE.
        self.NUMBER_RADIUS = RADIUS * 0.7
        self.HANDLE_RADIUS = RADIUS * 0.2

        self.draw()

    def draw(self, milliseconds=0):
        # CALCULATE ANGLE.
        seconds = milliseconds / 1000
        angle = (seconds % 60) * 6
        # DISCARD BEFORE DRAWING.
        self.delete(ctk.ALL)
        # DRAW.
        self.draw_border()
        self.draw_handle(angle)
        self.draw_milestone(milliseconds)
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
                # DRAW MARK.
                inner_x = self.CENTER[0] + self.INN_RADIUS * cos_alpha
                inner_y = self.CENTER[1] + self.INN_RADIUS * sin_alpha
                self.create_line(
                    (outer_x, outer_y),
                    (inner_x, inner_y),
                    fill=WHITE,
                    width=LINE_WIDTH,
                )
                # DRAW NUMBER.
                number_x = self.CENTER[0] + self.NUMBER_RADIUS * cos_alpha
                number_y = self.CENTER[1] + self.NUMBER_RADIUS * sin_alpha
                self.create_text(
                    (number_x, number_y),
                    fill=WHITE,
                    text=f"{angle // 6}",
                    font=f'"{FONT}" {CLOCK_FONT_SIZE}',
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

    def draw_handle(self, angle):
        sin_alpha = sin(radians(angle - 90))
        cos_alpha = cos(radians(angle - 90))
        # OUTER POINT.
        outer_x = self.CENTER[0] + self.OUT_RADIUS * cos_alpha
        outer_y = self.CENTER[1] + self.OUT_RADIUS * sin_alpha
        # INNER POINT.
        inner_x = self.CENTER[0] - self.HANDLE_RADIUS * cos_alpha
        inner_y = self.CENTER[1] - self.HANDLE_RADIUS * sin_alpha
        self.create_line(
            (inner_x, inner_y),
            (outer_x, outer_y),
            fill=ORANGE,
            width=LINE_WIDTH,
        )

    def draw_milestone(self, milliseconds):
        self.create_text(
            (self.CENTER[0], self.CENTER[1] + 50),
            fill=WHITE,
            text=Clock.strftime(milliseconds),
            font=f'"{FONT}" {TIME_FONT_SIZE} bold',
            anchor=ctk.CENTER,
        )

    @staticmethod
    def strftime(milliseconds):
        # SPLIT TIME INTO COMPONENTS.
        seconds, remainders = divmod(milliseconds, 1000)
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        # FORMAT TIME.
        seconds = f"{seconds:02} . {remainders // 10:02}"
        minutes = f"{minutes:02} : " if minutes > 0 or hours > 0 else ""
        hours = f"{hours:02} : " if hours > 0 else ""

        return hours + minutes + seconds


class LapContainer(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(master=parent, fg_color=BLACK)
        self.grid(row=2, column=0, sticky=ctk.NSEW, padx=5, pady=5)
        # WIDGET.
        self.canvas = None

    def clear(self):
        if self.canvas:
            self.canvas.pack_forget()

    def draw_list(self, laps_list):
        # CLEAR BEFORE DRAWING.
        self.clear()
        # CALCULATE DATA.
        ITEM_NUMBER = len(laps_list)
        LIST_HEIGHT = ITEM_NUMBER * LAP_ITEM_HEIGHT
        IS_SCROLLABLE = LIST_HEIGHT > self.winfo_height()
        SCROLL_HEIGHT = max(LIST_HEIGHT, self.winfo_height())
        # CREATE CANVAS.
        self.canvas = ctk.CTkCanvas(
            master=self,
            background=BLACK,
            bd=0,
            highlightthickness=0,
            relief=ctk.RIDGE,
            scrollregion=(0, 0, self.winfo_width(), SCROLL_HEIGHT),
        )
        self.canvas.pack(expand=True, fill=ctk.BOTH)
        # SCROLL BAR.
        if IS_SCROLLABLE:
            self.canvas.bind_all(
                "<MouseWheel>",
                lambda event: self.canvas.yview_scroll(-int(event.delta / 60), "units"),
            )
        # CREATE DATA FRAME.
        ITEM_FONT = ctk.CTkFont(FONT, 14, "bold")
        frame = ctk.CTkFrame(master=self, fg_color=BLACK)
        for index, item in enumerate(laps_list):
            is_final = index == ITEM_NUMBER - 1
            self.draw_item(frame, item, is_final, ITEM_FONT)
        # DRAW DATA FRAME IN CANVAS.
        self.canvas.create_window(
            (0, 0),
            width=self.winfo_width(),
            height=LIST_HEIGHT,
            window=frame,
            anchor=ctk.NW,
        )

    def draw_item(self, parent, item, is_final, font):
        item_frame = ctk.CTkFrame(master=parent, fg_color=BLACK)
        data_frame = ctk.CTkFrame(master=item_frame, fg_color=BLACK)
        data_frame.pack(expand=ctk.TRUE, fill=ctk.BOTH, pady=5)
        item_frame.pack(fill=ctk.X)
        # DISPLAY DATA.
        ctk.CTkLabel(
            master=data_frame,
            text=f"{item[0]} {item[1]}",
            font=font,
        ).pack(side=ctk.LEFT, padx=10)
        ctk.CTkLabel(
            master=data_frame,
            text=f"{Clock.strftime(item[2])}",
            font=font,
        ).pack(side=ctk.RIGHT, padx=10)
        # DISPLAY LINE.
        if not is_final:
            ctk.CTkFrame(
                master=item_frame,
                height=2,
                fg_color=GREY,
            ).pack(side=ctk.BOTTOM, fill=ctk.X)
