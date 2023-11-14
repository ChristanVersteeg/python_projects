import tkinter as tk
import keyboard as key
import os

position_file = os.path.join(os.environ['LOCALAPPDATA'], 'DontForgetToTurnOffPacePingsParrot', 'window_position.txt')
if not os.path.exists(os.path.dirname(position_file)): os.makedirs(os.path.dirname(position_file))
if not os.path.exists(position_file):
    with open(position_file, 'w') as file:
        file.write("0,0")
        
warn_window = None

def save_position(position):
    with open(position_file, "w") as file:
        file.write(f"{position[0]},{position[1]}")

def load_position():
    with open(position_file, "r") as file:
        position = file.read().split(',')
        return int(position[0]), int(position[1])

def make_label_window(text, position=None):
    window = tk.Toplevel()
    window.overrideredirect(True)
    window.attributes('-topmost', True)
    label = tk.Label(window, text=text, bg="lightgrey", borderwidth=2, relief="solid")
    label.pack()

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
    global warn_window
    if warn_window is None:
        # Load the position and create the window
        position = load_position()
        warn_window = make_label_window("PARROT DO NOT FORGET TO DISABLE/ENABLE YOUR PACE PINGS YOU UTTER BUFFOON", position)
    else:
        # Save the position and destroy the window
        save_position((warn_window.winfo_x(), warn_window.winfo_y()))
        warn_window.destroy()
        warn_window = None

key.add_hotkey('9', toggle_window)

root = tk.Tk()
root.withdraw()

root.mainloop()