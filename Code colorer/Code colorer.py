#classes, variables, keywords, if-for-return, methods, locals, structs, numbers
##4dc9b0, #dcdcdc, #569cd6, #d8a0df, #dcdcaa, #9cdcfe, #86c691, #b5cea8

import pyautogui as auto; auto.PAUSE = 0.1
import keyboard
from time import sleep
import tkinter as tk
from PIL import Image, ImageTk

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
keyboard.on_press(toggle_tab_bar)

def display_image():
    global root
    root = tk.Tk()
    
    root.title("Map")
    root.attributes('-topmost', True)
    
    img = Image.open("ColorMap.png")

    max_size = (300, 300) 
    img.thumbnail(max_size, Image.LANCZOS)

    photo = ImageTk.PhotoImage(img)

    label = tk.Label(root, image=photo)
    label.pack()

    root.mainloop()
display_image()