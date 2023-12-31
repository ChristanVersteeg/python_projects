#structs, variables, methods, classes, locals,  keywords, if/for,  comments, numbers, #line numbers        
#9cdcfe,  #dcdcdc,   #dcdcaa, #4dc9b0, #86c691, #569cd6,  #d8a0df, #4F9E46,  #b5cea8, #848480              

import pyautogui as auto; auto.PAUSE = 0.1
import keyboard
from time import sleep
import tkinter as tk
from PIL import Image, ImageTk
import re

root = None
tab_bar = True

def execute_commands(count):
    sleep(0.5)
    auto.hotkey('alt', '5')
    auto.press('down')
    auto.press('right', count)
    auto.press('enter')

for i in range(1, 11):
    keyboard.add_hotkey(f'ctrl+f{i}', lambda i=i: execute_commands(i-1))

def toggle_tab_bar(event):
    if event.name == 'esc': 
        global tab_bar
        root.overrideredirect(tab_bar)
        
        tab_bar = not tab_bar
        
        x, y = re.findall(r'[+-]\d+',  root.geometry())
        
        if int(x) <= 0: return
        
        value = -10 if tab_bar else 10
        x = ('+' if int(x) + value >= 0 else '') + str(int(x) + value)
        
        root.geometry(x + y)
keyboard.on_press(toggle_tab_bar)

def display_image():
    global root
    root = tk.Tk()
    
    root.title("Map")
    root.attributes('-topmost', True)
    root.resizable(False, False)
    
    img = Image.open("ColorMap.png")

    max_size = (300, 300) 
    img.thumbnail(max_size, Image.LANCZOS)

    photo = ImageTk.PhotoImage(img)

    label = tk.Label(root, image=photo)
    label.pack()

    root.mainloop()
display_image()

keyboard.wait()