import tkinter as tk
from tkinter import font
import keyboard as key
import json
import os

def save_position(position):
    open(position_file, "w").write(f"{position[0]},{position[1]}")

def load_position():
    return list(map(int, open(position_file, "r").read().split(',')))

def file_to_app_data_path(file):
   return os.path.join(os.environ['LOCALAPPDATA'], 'OBSKeyTriggeredTextOverlay', file)

json_file = file_to_app_data_path('label_settings.json')
with open(json_file, 'r') as file:
    settings = json.load(file)
    text = settings['text']
    fg_color = settings['fg_color']
    bg_color = settings['bg_color']
    font_size = settings['font_size']
    font_family = settings['font_family']
    font_weight = settings['font_weight']
    font_slant = settings['font_slant']
    font_overstrike = settings['font_overstrike']
    font_underline = settings['font_underline']
    border_size = settings['border_size']
    relief_type = settings['relief_type']
    alpha = settings['alpha']
    hotkey = settings['hotkey']

position_file = file_to_app_data_path('window_position.txt')
if not os.path.exists(os.path.dirname(position_file)): os.makedirs(os.path.dirname(position_file))
if not os.path.exists(position_file): open(position_file, 'w').write("0,0")
position = load_position()
old_position = position
warn_window = None

def create_tkinter_loop():
    root = tk.Tk()
    root.withdraw()
    root.mainloop()

def create_label():
    window = tk.Toplevel()
    window.overrideredirect(True)
    window.attributes('-topmost', True)
    window.geometry(f"+{position[0]}+{position[1]}")
    window.attributes('-alpha', alpha)
    label_font = font.Font(family=font_family, size=font_size, weight=font_weight, slant=font_slant, overstrike=font_overstrike, underline=font_underline)
    label = tk.Label(window, text=text, bg=bg_color, fg=fg_color, borderwidth=border_size, relief=relief_type, font=label_font)
    label.pack()
    
    return window, label

def label_movement(window, label):
    window.drag_position = None
    
    def on_press_release(event):
        global position
        window.drag_position = (event.x, event.y) if window.drag_position is None else None
        position = window.winfo_x(), window.winfo_y()
        
    def on_move(event):
        deltax, deltay = event.x - window.drag_position[0], event.y - window.drag_position[1]
        window.geometry(f"+{window.winfo_x() + deltax}+{window.winfo_y() + deltay}")

    label.bind('<ButtonPress-1>', on_press_release)
    label.bind('<ButtonRelease-1>', on_press_release)
    label.bind('<B1-Motion>', on_move)
    
def make_label_window():
    window, label = create_label()
    
    label_movement(window, label)

    return window

def toggle_window():
    global warn_window
    global old_position
    
    if warn_window is None:
        warn_window = make_label_window()
    else:
        warn_window.destroy()
        warn_window = None
        if(old_position is not position):
            print(old_position, position)
            save_position(position)
            old_position = position
key.add_hotkey(hotkey, toggle_window)

create_tkinter_loop()