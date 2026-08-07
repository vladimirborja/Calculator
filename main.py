import os
import sys
import subprocess
import tkinter as tk
from tkinter import messagebox

VIDEO_FILENAME = "jb_suarez.mp4"         
PLAY_ON_EVERY_EQUALS = False             
TRIGGER_RESULT = 4                       


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
            os.startfile(video_path) 
        elif sys.platform == "darwin":
            script = f'tell application "QuickTime Player"\n open POSIX file "{video_path}"\n play document 1\n activate\nend tell'
            try:
                subprocess.Popen(["osascript", "-e", script])
            except Exception:
                subprocess.Popen(["open", video_path])  
        else:
            subprocess.Popen(["xdg-open", video_path])
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
            raw_expr = self.expression
            allowed = set("0123456789.+-*/() ")
            if not all(c in allowed for c in self.expression):
                raise ValueError("Invalid characters")

            result = eval(self.expression, {"__builtins__": {}}, {})

            clean_expr = raw_expr.replace(" ", "")
            if PLAY_ON_EVERY_EQUALS or clean_expr == "2+2" or result == TRIGGER_RESULT:
                self.expression = ""
                self.display_var.set("0")
                play_meme_video()
            else:
                self.display_var.set(str(result))
                self.expression = str(result)

        except Exception:
            self.display_var.set("Error")
            self.expression = ""


if __name__ == "__main__":
    app = Calculator()
    app.mainloop()