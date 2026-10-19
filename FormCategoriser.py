import time
import pyautogui

# Safety feature: Move your mouse to any of the 4 corners of your screen
# to instantly abort the script if something goes wrong.
pyautogui.FAILSAFE = True

# ==================== CONFIGURATION ====================
COORDINATES = [
    (565, 209),  # 1st click
    (840, 76),  # 2nd click
    (1417, 143),  # 3rd click
    (1413, 208),  # 4th click
    (2089, 80),  # 5th click
]

# Adjust these pause times (in seconds) if your browser needs more time to load/respond
PAUSE_BETWEEN_CLICKS = 0.5
PAUSE_BETWEEN_TABS = 1.0
# =======================================================


def main():
  print("--- AUTOMATION STARTING ---")
  print("You have 3 seconds to switch to your browser/target window!")
  time.sleep(3)

  # Loop 19 times
  for iteration in range(1, 20):
    print(f"\n[Cycle {iteration}/19] Switching tab...")

    # 1. Press Ctrl + Tab to go to the next tab
    pyautogui.hotkey("ctrl", "tab")
    time.sleep(PAUSE_BETWEEN_TABS)

    # 2. Loop through and click each of the 5 coordinates
    for index, (x, y) in enumerate(COORDINATES, start=1):
      print(f"  -> Clicking position {index}: X={x}, Y={y}")
      pyautogui.click(x, y)
      time.sleep(PAUSE_BETWEEN_CLICKS)

  print("\n--- AUTOMATION FINISHED ---")


if __name__ == "__main__":
  main()