import pyautogui; pyautogui.PAUSE = 0.01;
import keyboard
from time import sleep

paused = False

def interact(event):
    global paused 
    
    if event.event_type == keyboard.KEY_DOWN:
        if event.name == 'i':
            paused = not paused

        if event.name == 'e' and not paused:
            sleep(0.2)
            pyautogui.moveTo(880, 400)
            sleep(0.2)
            pyautogui.click()
            
keyboard.hook(interact)

keyboard.wait()         