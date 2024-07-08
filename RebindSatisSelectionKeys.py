import keyboard
import pyautogui

pyautogui.PAUSE = 0.05

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

keyboard.on_press_key('1', lambda _: scroll('1'))
keyboard.on_press_key('2', lambda _: scroll('2'))
keyboard.on_press_key('3', lambda _: scroll('3'))
keyboard.on_press_key('4', lambda _: scroll('4'))
keyboard.on_press_key('5', lambda _: scroll('5'))

keyboard.wait('-')