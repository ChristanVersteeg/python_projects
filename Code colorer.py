#classes, variables, keywords, if-for-return, methods, locals, structs, numbers
##4dc9b0, #dcdcdc, #569cd6, #d8a0df, #dcdcaa, #9cdcfe, #86c691, #b5cea8

import pyautogui as auto; auto.PAUSE = 0.1
import keyboard
from time import sleep

def execute_commands(count):
    sleep(0.5)
    auto.hotkey('alt', '5')
    auto.press('down')
    auto.press('right', count)
    auto.press('enter')

for i in range(1, 11):
    keyboard.add_hotkey(f'ctrl+f{i}', lambda i=i: execute_commands(i-1))
    
keyboard.wait()