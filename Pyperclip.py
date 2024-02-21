import pyperclip

while(True):
    
    pyperclip.waitForNewPaste()
    with open("transcript.txt", 'a') as f: f.write(f"{pyperclip.paste()}\n")