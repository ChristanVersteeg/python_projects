import tkinter as tk
import keyboard as key

warn_window = None

def make_label_window(text):
    window = tk.Toplevel()
    window.overrideredirect(True)
    window.attributes('-topmost', True)
    label = tk.Label(window, text=text, bg="lightgrey", borderwidth=2, relief="solid")
    label.pack()

    def start_move(event):
        window.x = event.x
        window.y = event.y

    def stop_move(event):
        window.x = None
        window.y = None

    def on_move(event):
        deltax = event.x - window.x
        deltay = event.y - window.y
        x = window.winfo_x() + deltax
        y = window.winfo_y() + deltay
        window.geometry(f"+{x}+{y}")

    label.bind('<ButtonPress-1>', start_move)
    label.bind('<ButtonRelease-1>', stop_move)
    label.bind('<B1-Motion>', on_move)

    return window

def toggle_window():
    global warn_window
    if warn_window is None:
        # Create the window
        warn_window = make_label_window("PARROT DO NOT FORGET TO DISABLE/ENABLE YOUR PACE PINGS YOU UTTER BUFFOON")
    else:
        # Destroy the window
        warn_window.destroy()
        warn_window = None

key.add_hotkey('9', toggle_window)

root = tk.Tk()
root.withdraw()

root.mainloop()
