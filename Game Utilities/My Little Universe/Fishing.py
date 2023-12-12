import cv2
import numpy as np
import pyautogui
import time
import threading
import keyboard 
import re

# Function to print the mouse position when 'home' key is pressed
def print_mouse_position(event):
    if event.name == 'home': 
        mouse_position = ', '.join(re.findall(r'\d+', str(pyautogui.position())))
        print(mouse_position)

keyboard.on_press(print_mouse_position)

# Load the arrow images
arrows = {
    'up': cv2.imread('up.png', 0),
    'down': cv2.imread('down.png', 0),
    'left': cv2.imread('left.png', 0),
    'right': cv2.imread('right.png', 0)
}

startX, startY = 1805, 1683  # Replace with the actual coordinates

def find_arrow(screen, arrow_image, direction):
    res = cv2.matchTemplate(screen, arrow_image, cv2.TM_CCOEFF_NORMED)
    if np.max(res) >= 0.8:
        print(f"{direction} arrow detected.")
        return True
    return False

def display_debug_window():
    while not exit_flag:
        if debug_screen is not None:
            cv2.imshow('Debug Window', debug_screen)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows()

exit_flag = False
debug_screen = None

# Start debug window thread
threading.Thread(target=display_debug_window, daemon=True).start()

try:
    while True:
        screen = pyautogui.screenshot(region=(startX, startY, 300, 300))
        screen = cv2.cvtColor(np.array(screen), cv2.COLOR_BGR2GRAY)

        # Store the screen in a variable for the debug window
        debug_screen = screen.copy()

        for direction, arrow_img in arrows.items():
            if find_arrow(screen, arrow_img, direction):
                pyautogui.press(direction)
                break

        time.sleep(0.1)
except KeyboardInterrupt:
    exit_flag = True
