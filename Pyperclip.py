import pyperclip

user_input = input("Type the word you want to gluckify: ")

print(f"Gluckified \"{user_input}\". It has been saved to the clipboard, you can paste it anywhere with CTRL+V.")

pyperclip.copy(f"gl{user_input}")