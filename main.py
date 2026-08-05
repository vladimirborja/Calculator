"""
JB SUAREZ Meme Calculator
--------------------------
A simple Tkinter calculator. Every time you press "=", it plays a
meme video (JB SUAREZ) using your system's default video player.

SETUP:
1. Put a video file named "jb_suarez.mp4" in the SAME FOLDER as this script.
   (Any meme clip you have rights to use works — just name it jb_suarez.mp4,
   or change VIDEO_FILENAME below to match your file.)
2. Run: python jb_suarez_calculator.py

Optional: set PLAY_ON_EVERY_EQUALS = False if you only want the meme to
play for a specific result (e.g. only when 2 + 2 = 4).
"""

import os
import sys
import subprocess
import tkinter as tk
from tkinter import messagebox

# ---------------- CONFIG ----------------
VIDEO_FILENAME = "jb_suarez.mp4"          # video file to play
PLAY_ON_EVERY_EQUALS = True               # True = play on every "=", False = only on TRIGGER_RESULT
TRIGGER_RESULT = 4                        # used only if PLAY_ON_EVERY_EQUALS is False (e.g. 2+2=4)
# -----------------------------------------


def play_meme_video():
    """Open the meme video with the OS default video player."""
    video_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), VIDEO_FILENAME)

    if not os.path.exists(video_path):
        messagebox.showwarning(
            "Video not found",
            f'Could not find "{VIDEO_FILENAME}" in this folder.\n\n'
            f"Add your JB SUAREZ video file here:\n{video_path}"
        )
        return

    try:
        if sys.platform.startswith("win"):
            os.startfile(video_path)  # Windows
        elif sys.platform == "darwin":
            subprocess.Popen(["open", video_path])  # macOS
        else:
            subprocess.Popen(["xdg-open", video_path])  # Linux
    except Exception as e:
        messagebox.showerror("Playback error", f"Couldn't open video:\n{e}")


class Calculator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("JB SUAREZ Calculator")
        self.resizable(False, False)
        self.configure(bg="#181818")

        self.expression = ""
        self.display_var = tk.StringVar(value="0")

        self._build_display()
        self._build_buttons()

    def _build_display(self):
        display = tk.Entry(
            self,
            textvariable=self.display_var,
            font=("Consolas", 30, "bold"),
            bd=0,
            justify="right",
            bg="#0d0d0d",
            fg="#ffffff",
            insertwidth=2,
            insertbackground="#ffffff",
            state="readonly",
            readonlybackground="#0d0d0d",
        )
        display.grid(row=0, column=0, columnspan=4, ipady=26, sticky="nsew", padx=10, pady=(10, 4))

    def _build_buttons(self):
        buttons = [
            ("C", 1, 0), ("(", 1, 1), (")", 1, 2), ("/", 1, 3),
            ("7", 2, 0), ("8", 2, 1), ("9", 2, 2), ("*", 2, 3),
            ("4", 3, 0), ("5", 3, 1), ("6", 3, 2), ("-", 3, 3),
            ("1", 4, 0), ("2", 4, 1), ("3", 4, 2), ("+", 4, 3),
            ("0", 5, 0), (".", 5, 1), ("⌫", 5, 2), ("=", 5, 3),
        ]

        for (text, row, col) in buttons:
            # Default: digit/dot keys — mid-dark gray, white text
            color = "#2d2d2d"
            text_color = "#ffffff"
            hover_color = "#3d3d3d"
            font_size = 18

            if text == "=":
                color = "#00c060"
                text_color = "#ffffff"
                hover_color = "#00e070"
                font_size = 20
            elif text in ("C", "⌫"):
                color = "#c0392b"
                text_color = "#ffffff"
                hover_color = "#e74c3c"
            elif text in ("+", "-", "*", "/", "(", ")"):
                color = "#2c3e50"
                text_color = "#7ec8e3"
                hover_color = "#3d5468"

            btn = tk.Button(
                self,
                text=text,
                font=("Consolas", font_size, "bold"),
                bg=color,
                fg=text_color,
                activebackground=hover_color,
                activeforeground=text_color,
                relief="flat",
                cursor="hand2",
                command=lambda t=text: self.on_button_press(t),
            )
            btn.grid(row=row, column=col, sticky="nsew", padx=5, pady=5, ipadx=12, ipady=14)

        for i in range(6):
            self.grid_rowconfigure(i, weight=1)
        for i in range(4):
            self.grid_columnconfigure(i, weight=1, minsize=80)

    def on_button_press(self, char):
        if char == "C":
            self.expression = ""
            self.display_var.set("0")

        elif char == "⌫":
            self.expression = self.expression[:-1]
            self.display_var.set(self.expression if self.expression else "0")

        elif char == "=":
            self.calculate()

        else:
            self.expression += char
            self.display_var.set(self.expression)

    def calculate(self):
        try:
            # Only allow safe characters in the expression
            allowed = set("0123456789.+-*/() ")
            if not all(c in allowed for c in self.expression):
                raise ValueError("Invalid characters")

            result = eval(self.expression, {"__builtins__": {}}, {})
            self.display_var.set(str(result))
            self.expression = str(result)

            # 🎬 Trigger the meme video
            if PLAY_ON_EVERY_EQUALS or result == TRIGGER_RESULT:
                play_meme_video()

        except Exception:
            self.display_var.set("Error")
            self.expression = ""


if __name__ == "__main__":
    app = Calculator()
    app.mainloop()