import keyboard as key
import pyautogui as auto;
from euclid3 import Vector2
import re

paused = False
chat_bin_coords = Vector2(230, 190)
delete_prompt_coords = Vector2(1125, 630)

def print_mouse_position(event):
    if event.name == 'home': 
        print(', '.join(re.findall(r'\d+', str(auto.position()))))
key.on_press(print_mouse_position)

def print_mouse_position(event):
    if event.name == 'end': 
        global paused
        paused = not paused
key. on_press(print_mouse_position)



def delete(event):
    def matches_any_key(*keys):
        return event.name in keys
       
    if(paused): return
    if not matches_any_key('delete', 'backspace', 'page up'): return

    if event.name == 'delete': #Removes first chat that is not selected
        auto.click(chat_bin_coords.x, chat_bin_coords.y)
    #And backspace removes first chat that is selected    
    if event.name != 'page up': #Removes chat that the cursor selects on top of the bin
        auto.click(chat_bin_coords.x, chat_bin_coords.y)
    else: 
        auto.click()
        x, y = auto.position()
    
    auto.click(delete_prompt_coords.x, delete_prompt_coords.y)
        
    if(event.name == 'page up'):
        auto.moveTo(x, y)
key.on_press(delete)

key.wait()