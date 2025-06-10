import tkinter as tk
from frontend.layout import BoilTimerApp

if __name__ == "__main__":
    root = tk.Tk()
    app = BoilTimerApp(root)
    root.mainloop()