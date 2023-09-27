import keyboard as key
import pyautogui as auto;
from euclid3 import Vector2
import re

chat_bin_coords = Vector2(230, 190)
delete_prompt_coords = Vector2(1125, 630)

def print_mouse_position(event):
    if event.name == 'home': 
        print(', '.join(re.findall(r'\d+', str(auto.position()))))
key.on_press(print_mouse_position)

def delete(event):
    if event.name == 'delete': 
        auto.click(chat_bin_coords.x, chat_bin_coords.y)
        auto.click(chat_bin_coords.x, chat_bin_coords.y)
        auto.click(delete_prompt_coords.x, delete_prompt_coords.y)
key.on_press(delete)

key.wait()