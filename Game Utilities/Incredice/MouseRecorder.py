import pyautogui
pyautogui.PAUSE = 0.00

import keyboard
import threading
import time
import sys

# Settings
SPEED_MULTIPLIER = 3.0  # 1.0 = normal speed, 2.0 = 2x faster, etc.
MIN_DELAY = 0.001       # Smallest delay to respect (after speeding up)

# Global state
recording = False 
playing_back = False
macro_data = []

def record_mouse_path():
    global recording, macro_data
    macro_data = []
    print("[INFO] Recording mouse path... Press 'f' again to stop.")
    last_pos = pyautogui.position()
    last_time = time.time()

    while recording:
        current_pos = pyautogui.position()
        now = time.time()
        if current_pos != last_pos:
            macro_data.append({
                'position': current_pos,
                'delay': now - last_time
            })
            last_pos = current_pos
            last_time = now
        time.sleep(0.01)

    print(f"[INFO] Recording stopped. {len(macro_data)} points captured.")

def play_mouse_path():
    global playing_back
    print(f"[INFO] Replaying at {SPEED_MULTIPLIER}x speed. Press 'f' to stop.")

    while playing_back:
        for step in macro_data:
            if not playing_back:
                print("[INFO] Playback stopped.")
                return

            adjusted_delay = step['delay'] / SPEED_MULTIPLIER
            if adjusted_delay >= MIN_DELAY:
                time.sleep(adjusted_delay)

            pyautogui.moveTo(step['position'])

        time.sleep(0.1)

def toggle_macro():
    global recording, playing_back

    if not recording and not playing_back:
        recording = True
        threading.Thread(target=record_mouse_path, daemon=True).start()

    elif recording:
        recording = False
        if macro_data:
            playing_back = True
            threading.Thread(target=play_mouse_path, daemon=True).start()
        else:
            print("[WARN] No data recorded.")

    elif playing_back:
        playing_back = False

def exit_script():
    global recording, playing_back
    recording = False
    playing_back = False
    print("[INFO] Exiting.")
    sys.exit(0)

def main():
    print("=== Mouse Macro Recorder ===")
    print(f"Press 'f' to toggle: record  play fff stop (Speed: {SPEED_MULTIPLIER}x)")
    print("Press 'esc' to quit.")

    keyboard.add_hotkey('f', toggle_macro)
    keyboard.add_hotkey('esc', exit_script)

    keyboard.wait()

if __name__ == "__main__":
    main()
