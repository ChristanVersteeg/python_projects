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
scan_area = []
clicked_positions = []

# Load templates once
templates = []
template_sizes = []
for tf in TEMPLATE_FILES:
    if os.path.exists(tf):
        tpl = cv2.imread(tf, cv2.IMREAD_GRAYSCALE)
        if tpl is not None:
            templates.append(tpl)
            template_sizes.append((tpl.shape[1], tpl.shape[0]))
        else:
            print(f"[ERROR] Failed to load template {tf}")
    else:
        print(f"[WARN] Template not found: {tf}")

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
        print(f"[INFO] Scan point {len(scan_area)} set at {pos}")
    else:
        print("[WARN] Scan area already set. Restart to reset.")

def scan_and_hover():
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
    screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2GRAY)

    matched_points = []

    threshold = 0.4  # Tune this as needed

    for template, (w, h) in zip(templates, template_sizes):
        res = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
        loc = np.where(res >= threshold)
        points = list(zip(*loc[::-1]))

        rects = []
        for pt in points:
            rects.append([pt[0], pt[1], w, h])

        rects, _ = cv2.groupRectangles(rects, groupThreshold=1, eps=0.5)

        for (x, y, w_rect, h_rect) in rects:
            screen_x = left + x + w_rect // 2
            screen_y = top + y + h_rect // 2
            matched_points.append((screen_x, screen_y))

    filtered_points = []
    for p in matched_points:
        if all(abs(p[0] - fp[0]) > CLICK_MARGIN or abs(p[1] - fp[1]) > CLICK_MARGIN for fp in filtered_points):
            filtered_points.append(p)

    pyautogui.PAUSE = 0.01
    for (x, y) in filtered_points:
        pyautogui.moveTo(x, y)
        print(f"[HOVER] at ({x}, {y})")

    clicked_positions = filtered_points
    print(f"[INFO] Hovered over {len(filtered_points)} positions.")

def main():
    print("ssDice Auto Hover Ready")
    print("Press 's' twice to define scan area (top-left then bottom-right).")
    print("Press 'D' to stop the auto-hover loop.")
    print("Waiting for scan area to be set...")

    keyboard.add_hotkey('s', set_scan_point)

    # Wait for scan area to be set
    while len(scan_area) < 2:
        if keyboard.is_pressed('D'):
            exit_script()
        time.sleep(0.1)

    print("[INFO] Starting auto-hover loop.")

    try:
        while True:
            if keyboard.is_pressed('D'):
                print("[INFO] 'D' pressed. Exiting.")
                break
            scan_and_hover()
    except KeyboardInterrupt:
        print("[INFO] Interrupted by user.")
    finally:
        exit_script()

def exit_script():
    print("[INFO] Exiting script.")
    sys.exit(0)

if __name__ == "__main__":
    main()
