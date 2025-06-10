import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import random
from logic.foods import BOILING_TIMES, BOILING_IMAGES, BOILING_INSTRUCTIONS, FRYING_TIMES, FRYING_IMAGES, FRYING_INSTRUCTIONS
from logic.timer import Timer

class BoilTimerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Cooking Timer")
        self.root.geometry("700x600")
        self.root.configure(bg="#ffe6ea")

        self.mode = "boiling"  # Default mode
        self.food_var = tk.StringVar()
        self.quotes = [
            "You are gonna cook this perfectly!💕",
            "You’re doing amazing, chef 👩‍🍳✨",
            "Hey beautiful, you're killing it! 🔥",
            "Pour a little love into the pot — you got this 💖",
            "Can’t wait to eat this with you 😋",
            "I can taste whether you put in love or not!🍽️💗"
        ]

        self.timer = Timer(self.update_timer_display, self.timer_done)
        self.create_widgets()
        self.set_mode("boiling")  # Initialize with boiling mode

    def create_widgets(self):
        font_label = ("Segoe UI", 12)
        font_timer = ("Segoe UI", 36, "bold")
        font_button = ("Segoe UI", 11)

        mode_frame = tk.Frame(self.root, bg="#ffe6ea")
        mode_frame.pack(pady=10)

        self.boil_btn = tk.Button(mode_frame, text="Boiling 🔥", command=lambda: self.set_mode("boiling"),
                                  font=font_button, bg="#ffb3c6", fg="#000000", relief="raised", padx=10)
        self.boil_btn.pack(side="left", padx=10)
        self.fry_btn = tk.Button(mode_frame, text="Frying 🍳", command=lambda: self.set_mode("frying"),
                                 font=font_button, bg="#ffe6ea", fg="#000000", relief="raised", padx=10)
        self.fry_btn.pack(side="left", padx=10)

        main_frame = tk.Frame(self.root, bg="#ffe6ea")
        main_frame.pack(fill="both", expand=True, padx=20)
        left_panel = tk.Frame(main_frame, bg="#ffe6ea")
        left_panel.grid(row=0, column=0, sticky="n")
        right_panel = tk.Frame(main_frame, bg="#ffe6ea")
        right_panel.grid(row=0, column=1, padx=30, sticky="n")

        tk.Label(left_panel, text="Select Food", bg="#ffe6ea", fg="#000000", font=font_label).pack(pady=5)
        self.food_menu = ttk.Combobox(left_panel, textvariable=self.food_var, state="readonly")
        self.food_menu.pack(ipady=4)
        self.food_menu.bind("<<ComboboxSelected>>", lambda e: self.update_display())

        #Food
        self.image_label = tk.Label(left_panel, bg="#ffe6ea")
        self.image_label.pack(pady=10)

        #Timer
        self.timer_label = tk.Label(left_panel, text="00:00", font=font_timer, bg="#ffe6ea", fg="#884d88")
        self.timer_label.pack(pady=5)

        #Progress bar
        self.progress_bar = ttk.Progressbar(left_panel, orient="horizontal", length=200, mode="determinate")
        self.progress_bar.pack(pady=5)

        self.quote_label = tk.Label(left_panel, text="", wraplength=250, justify="center",
                                    bg="#ffe6ea", fg="#884d88", font=("Segoe UI", 10, "italic"))
        self.quote_label.pack(pady=5)

        # Buttons
        self.start_button = tk.Button(left_panel, text="Start Timer", font=font_button,
                                      bg="#66ffcc", fg="#000000", command=self.start_timer)
        self.start_button.pack(pady=3)

        self.stop_button = tk.Button(left_panel, text="Stop Timer", font=font_button,
                                     bg="#ff6666", fg="#000000", command=self.stop_timer, state="disabled")
        self.stop_button.pack(pady=3)

        self.reset_button = tk.Button(left_panel, text="Reset Timer", font=font_button,
                                      bg="#cccccc", fg="#000000", command=self.reset_timer)
        self.reset_button.pack(pady=3)

        # Instruction display
        tk.Label(right_panel, text="Instructions", bg="#ffe6ea", fg="#000000", font=("Segoe UI", 12, "bold")).pack(anchor="nw")
        self.instruction_text = tk.Label(right_panel, text="", wraplength=220, justify="left",
                                         bg="#ffe6ea", fg="#444444", font=("Segoe UI", 10))
        self.instruction_text.pack(anchor="nw", pady=5)
        try:
            from PIL import Image, ImageTk
            import os

            icon_path = os.path.join("assets", "corner_icon.png")
            icon_img = Image.open(icon_path).resize((64, 64))
            self.corner_icon = ImageTk.PhotoImage(icon_img)
            self.icon_label = tk.Label(self.root, image=self.corner_icon, bg="#ffe6ea", borderwidth=0)
            self.icon_label.place(relx=1.0, rely=1.0, anchor="se", x=-10, y=-10)
        except Exception as e:
            print(f"Corner icon failed to load: {e}")

    def set_mode(self, mode):
        self.mode = mode
        self.update_mode_buttons()
        if mode == "boiling":
            self.food_data = BOILING_TIMES
            self.food_images = BOILING_IMAGES
            self.food_instructions = BOILING_INSTRUCTIONS
        else:
            self.food_data = FRYING_TIMES
            self.food_images = FRYING_IMAGES
            self.food_instructions = FRYING_INSTRUCTIONS
        self.food_menu['values'] = list(self.food_data.keys())
        self.food_var.set(list(self.food_data.keys())[0])
        self.update_display()

    def update_mode_buttons(self):
        active_color = "#ffb3c6"
        inactive_color = "#ffe6ea"
        if self.mode == "boiling":
            self.boil_btn.configure(bg=active_color)
            self.fry_btn.configure(bg=inactive_color)
        else:
            self.boil_btn.configure(bg=inactive_color)
            self.fry_btn.configure(bg=active_color)

    def update_display(self):
        food = self.food_var.get()
        path = self.food_images.get(food)
        try:
            img = Image.open(path).resize((200, 150))
            photo = ImageTk.PhotoImage(img)
            self.image_label.config(image=photo)
            self.image_label.image = photo
        except:
            self.image_label.config(image="", text="Image not found", fg="white")
        instruction = self.food_instructions.get(food, "No instructions available.")
        self.instruction_text.config(text=instruction)

    def update_timer_display(self, text):
        self.timer_label.config(text=text)
        if hasattr(self, "total_time") and self.total_time > 0 and self.timer.time_left >= 0:
            elapsed = self.total_time - self.timer.time_left
            percent = (elapsed / self.total_time) * 100
            self.progress_bar["value"] = percent
        else:
            self.progress_bar["value"] = 0

    def timer_done(self):
        self.start_button.config(state="normal")
        self.stop_button.config(state="disabled")

    def start_timer(self):
        food = self.food_var.get()
        duration = self.food_data[food]
        self.total_time = duration
        self.quote_label.config(text=random.choice(self.quotes))
        self.start_button.config(state="disabled")
        self.stop_button.config(state="normal")
        self.timer.start(duration)

    def stop_timer(self):
        self.timer.stop()
        self.start_button.config(state="normal")
        self.stop_button.config(state="disabled")

    def reset_timer(self):
        self.timer.stop()
        self.update_timer_display("00:00")
        self.progress_bar["value"] = 0
        self.start_button.config(state="normal")
        self.stop_button.config(state="disabled")
