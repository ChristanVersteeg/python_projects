import pyautogui as auto; auto.PAUSE = 0.2
import keyboard
from time import sleep

             #classes, variables, keywords, if-for-return, methods, locals, structs, numbers
             #0, 1, 2, 3, 4, 5, 6, 7
#HEX_CODES = ['#4dc9b0', '#dcdcdc', '#569cd6', '#d8a0df', '#dcdcaa', '#9cdcfe', '#86c691', '#b5cea8']
             #660, 305-687,297

color = [1, 2, 3, 5 ,5 ,5 , 5, 5, 5, 5, 5]
running = True

def on_key_event(event):
    if event.event_type == keyboard.KEY_DOWN and event.name == "s":
        global running
        running = False
keyboard.on_press(on_key_event)

sleep(2)
for i in range(len(color)):
    if(not running): break
    auto.hotkey('shift', 'right')
    auto.click(642, 176)
    auto.click(662 + 26*color[i], 300)
    auto.press('right')

