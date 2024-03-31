import pyautogui as auto; auto.PAUSE = 0.15;
import keyboard as key

# For configuration purposes.
#def print_mouse_position(event):
#    if event.name == 's': print(auto.position())
#key.on_press(print_mouse_position)

running = True

sources = [
    "Code of Conduct",
    "Data Analist voor",
    "Datalek bol.com: adressen",
    "Grootste Nederlandse webwinkels",
    "https://www.netapp.com",
    "Understand how structured",
    "Werk aan ontelbare",
    "avg hoofdstuk 2",
    "Register van de",
    "careers.bol.com ",
    "Privacybeleid bol.com",
    "Bol.com: voor 27%",
    "Big Data in"
]

def click(x, y, source = ""):
    if not running: return
    
    auto.click(x, y)
    
    if source != "": 
        auto.hotkey('ctrl', 'a')
        auto.press('backspace')
        auto.write(source)

def stop(_):
    global running
    running = False
key.on_press_key('2', stop)

key.wait('1')
for source in sources:
    click(112, 76, source)
    click(97, 197)
    click(642, 205)

key.wait()