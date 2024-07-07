import keyboard
import pyautogui; pyautogui.PAUSE = 0.05

current_slot = 1

def scroll_to_slot(target_slot):
    global current_slot
    scroll_units = target_slot - current_slot
    if scroll_units > 0:
        for _ in range(scroll_units):
            pyautogui.scroll(1)
    elif scroll_units < 0:
        for _ in range(-scroll_units):
            pyautogui.scroll(-1)
    current_slot = target_slot

def scroll(key):
    target_slot = int(key)
    scroll_to_slot(target_slot)

for key in ['1', '2', '3', '4', '5']:
    keyboard.add_hotkey(key, lambda k=key: scroll(k))

keyboard.wait('-')