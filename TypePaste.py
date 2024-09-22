from pyperclip import paste
import keyboard

hotkey = 'alt+v'

def write_copied_text():
    keyboard.write(paste())
keyboard.add_hotkey('alt+v', write_copied_text)

print(f"Press {hotkey.upper()} to paste your last copied text. (Since program boot).")

keyboard.wait()