import keyboard

index = 0

trigger_key = 'space'

text_file = 'display.txt' 

display_texts = [
    "This",
    "Shows",
    "How",
    "Versatile",
    "Python",
    "Is"
    ]
display_texts_length = len(display_texts)

def display_next_text(event):
    global index
    
    index += 1
    
    with open(text_file, 'w') as f: f.write(display_texts[index % display_texts_length])
    
keyboard.on_press_key(trigger_key, display_next_text, suppress=True)

def display_text_by_key(event):
    global index
    
    index = int(event.name)
    
    with open(text_file, 'w') as f: f.write(display_texts[index])
    
for i in range(10):
    keyboard.on_press_key(str(i), display_text_by_key, suppress=True)

keyboard.wait()