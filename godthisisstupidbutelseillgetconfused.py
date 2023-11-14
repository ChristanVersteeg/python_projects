import tkinter as tk
import keyboard as key

warn_window = None
last_position = None  # Variable to store the last position

def make_label_window(text, position=None):
    window = tk.Toplevel()
    window.overrideredirect(True)
    window.attributes('-topmost', True)
    label = tk.Label(window, text=text, bg="lightgrey", borderwidth=2, relief="solid")
    label.pack()

    # Set initial position if provided
    if position:
        window.geometry(f"+{position[0]}+{position[1]}")

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
    global warn_window, last_position
    if warn_window is None:
        # Create the window with the last saved position
        warn_window = make_label_window("PARROT DO NOT FORGET TO DISABLE/ENABLE YOUR PACE PINGS YOU UTTER BUFFOON", last_position)
    else:
        # Save the current position before destroying
        last_position = (warn_window.winfo_x(), warn_window.winfo_y())
        warn_window.destroy()
        warn_window = None

key.add_hotkey('9', toggle_window)

root = tk.Tk()
root.withdraw()

root.mainloop()
