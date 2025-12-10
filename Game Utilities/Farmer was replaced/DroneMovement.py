import keyboard
import pyautogui
import time
import threading

# Safety: moving mouse to top-left corner aborts pyautogui actions
pyautogui.FAILSAFE = True

CLICK_INTERVAL = 0.05  # seconds between clicks while holding

keys = ['w', 'a', 's', 'd']
coords = {}
is_held = {k: False for k in keys}  # track whether each key is currently held


print("=== COORDINATE SETUP ===")
print("You'll record 4 positions, in this order: W, A, S, D")
print("For each one: move your mouse to the desired spot, then press 'r' to save it.\n")

# Step 1: record 4 coordinates using the 'r' key
for key in keys:
    print(f"Move your mouse to the position for key '{key.upper()}', then press 'r'...")
    keyboard.wait('r')  # wait until 'r' is pressed
    x, y = pyautogui.position()
    coords[key] = (x, y)
    print(f"Recorded {key.upper()} -> ({x}, {y})")
    time.sleep(0.3)  # small delay to avoid double-trigger on 'r'

print("\n=== HOTKEYS ACTIVE ===")
print("Hold W / A / S / D to repeatedly click at their recorded coordinates.")
print(f"Click interval: {CLICK_INTERVAL:.3f} seconds while held.")
print("These keypresses are captured and will NOT reach other apps.")
print("Press ESC to quit.\n")


def click_loop(key: str):
    """Loop that clicks while the given key is held."""
    x, y = coords[key]
    # Optional: immediate click when pressed
    while is_held[key]:
        print(f"{key.upper()} held -> clicking at ({x}, {y})")
        pyautogui.click(x, y)
        time.sleep(CLICK_INTERVAL)


def make_on_key_down(k: str):
    def handler(event):
        # Ignore auto-repeats; only start a loop if wasn't already held
        if not is_held[k]:
            is_held[k] = True
            t = threading.Thread(target=click_loop, args=(k,), daemon=True)
            t.start()
    return handler


def make_on_key_up(k: str):
    def handler(event):
        is_held[k] = False
    return handler


# Bind press/release handlers for each key, suppressing the key events
for k in keys:
    keyboard.on_press_key(k, make_on_key_down(k), suppress=True)
    keyboard.on_release_key(k, make_on_key_up(k), suppress=True)

# Keep the script running until ESC is pressed (ESC is NOT suppressed)
keyboard.wait('esc')
print("Exiting...")
