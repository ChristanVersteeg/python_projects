import time
import keyboard
import pydirectinput
import vgamepad as vg

toggle = False

def toggle_script():
    """
    Toggle the 'toggle' variable when the 'Home' key is pressed.
    """
    global toggle
    toggle = not toggle
    print(f"[Toggle] => {toggle}")

def main():
    gamepad = vg.VX360Gamepad()
    keyboard.add_hotkey('home', toggle_script)

    print(
        "Mappings:\n"
        "  Arrow Keys  -> D-Pad\n"
        "  Numpad 4    -> Left Trigger\n"
        "  Numpad 6    -> Right Trigger\n"
        "  Numpad 5    -> A Button\n"
        "  Enter       -> Start Button\n\n"
        "Press 'Home' to toggle the repeating press of A + right-click every 500ms.\n"
        "Press CTRL+C (or close window) to exit.\n"
    )

    last_press_time = time.time()

    try:
        while True:
            # D-Pad: Arrow Keys
            if keyboard.is_pressed("up"):
                gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_UP)
            else:
                gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_UP)

            if keyboard.is_pressed("down"):
                gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_DOWN)
            else:
                gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_DOWN)

            if keyboard.is_pressed("left"):
                gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_LEFT)
            else:
                gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_LEFT)

            if keyboard.is_pressed("right"):
                gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_RIGHT)
            else:
                gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_RIGHT)

            # Left Trigger (Numpad 4)
            if keyboard.is_pressed("num 4"):
                gamepad.left_trigger(value=255)
            else:
                gamepad.left_trigger(value=0)

            # Right Trigger (Numpad 6)
            if keyboard.is_pressed("num 6"):
                gamepad.right_trigger(value=255)
            else:
                gamepad.right_trigger(value=0)

            # A Button (Numpad 5)
            if keyboard.is_pressed("num 5"):
                gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_A)
            else:
                gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_A)

            # Start Button (Enter)
            if keyboard.is_pressed("enter"):
                gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_START)
            else:
                gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_START)

            if toggle:
                now = time.time()
                if (now - last_press_time) >= 0.5:
                    gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_A)
                    gamepad.update()

                    pydirectinput.click(button='right')

                    gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_A)
                    gamepad.update()

                    last_press_time = now

            gamepad.update()
            time.sleep(0.01)
            
    except KeyboardInterrupt:
        print("\nExiting... Resetting controller.")
        gamepad.reset()
        gamepad.update()

if __name__ == "__main__":
    main()