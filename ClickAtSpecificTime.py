import pyautogui
import time

boolean = True

def click_at_10():
    # Infinite loop to keep checking the time
    
    while True:
        # Get the current time
        current_time = time.strftime('%H:%M')
        
        # Check if the current time is 10:00 AM
        if current_time == '10:00':
            # Perform the mouse click
            pyautogui.click()
            print("Mouse clicked at 10:00 AM.")
            break  # Exit the loop after clicking
        
        # Wait for a bit before checking the time again to avoid high CPU usage
        time.sleep(30)  # Check every 30 seconds

if __name__ == "__main__":
    click_at_10()
