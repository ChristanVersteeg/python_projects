import cv2
import numpy as np
import pyautogui
import keyboard
import time
import os
import sys

# Settings
CLICK_MARGIN = 100
TEMPLATE_FILES = [f'dice_{i}.png' for i in range(1, 7)]
clicked_positions = []
scan_area = []

def is_far_enough(pos, others):
    for ox, oy in others:
        if abs(pos[0] - ox) < CLICK_MARGIN and abs(pos[1] - oy) < CLICK_MARGIN:
            return False
    return True

def get_scan_area():
    if len(scan_area) != 2:
        return None
    x1, y1 = scan_area[0]
    x2, y2 = scan_area[1]
    return (min(x1, x2), min(y1, y2), max(x1, x2), max(y1, y2))

def set_scan_point():
    pos = pyautogui.position()
    if len(scan_area) < 2:
        scan_area.append(pos)
        print(f"[INFO] Point {len(scan_area)} set at {pos}")
    else:
        print("[WARN] Already have 2 scan points. Restart to reset.")

def scan_and_click():
    global clicked_positions
    area = get_scan_area()
    if area is None:
        print("[ERROR] Scan area not defined. Press 's' twice to set it.")
        return

    left, top, right, bottom = area
    width = right - left
    height = bottom - top

    print(f"[INFO] Scanning area: ({left}, {top}) to ({right}, {bottom})")

    screenshot = pyautogui.screenshot(region=(left, top, width, height))
    screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

    matched = 0

    for template_file in TEMPLATE_FILES:
        if not os.path.exists(template_file):
            print(f"[WARN] Missing template: {template_file}")
            continue

        template = cv2.imread(template_file)
        if template is None:
            print(f"[ERROR] Failed to load: {template_file}")
            continue

        res = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
        threshold = 0.3
        loc = np.where(res >= threshold)
        w, h = template.shape[1], template.shape[0]

    for pt in zip(*loc[::-1]):
        screen_x = left + pt[0] + w // 2
        screen_y = top + pt[1] + h // 2
        if is_far_enough((screen_x, screen_y), clicked_positions):
            pyautogui.moveTo(screen_x, screen_y)  # ← changed from click to hover
            clicked_positions.append((screen_x, screen_y))
            print(f"[HOVER] ({screen_x}, {screen_y}) using {template_file}")
            time.sleep(0.01)  # add a short delay to avoid too-fast movement


    print(f"[INFO] Done. {matched} clicks made.")

def exit_script():
    print("[INFO] Exiting script.")
    sys.exit(0)

def main():
    print("ssDice Auto Clicker Ready")
    print("Press 's' twice to define scan area (top-left then bottom-right).")
    print("Press 'f' to scan and click dice.")
    print("Press 'esc' to exit.")

    # Register hotkeys
    keyboard.add_hotkey('s', set_scan_point)
    keyboard.add_hotkey('f', scan_and_click)
    keyboard.add_hotkey('esc', exit_script)

    # Idle wait for hotkeys
    keyboard.wait()

if __name__ == "__main__":
    main()
