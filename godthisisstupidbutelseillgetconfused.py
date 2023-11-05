import tkinter as tk

def make_label_window(text):
    window = tk.Toplevel()
    window.overrideredirect(True)  # Remove window decorations
    window.attributes('-topmost', True)  # Keep window on top
    label = tk.Label(window, text=text, bg="lightgrey", borderwidth=2, relief="solid")
    label.pack()

    # Dragging functionality
    def start_move(event):
        window.x = event.x
        window.y = event.y

    def stop_move(event):
        window.x = None
        window.y = None

    def on_move(event):
        deltax = event.x - window.x
        deltay = event.y - window.y
        x = window.winfo_x() + deltax
        y = window.winfo_y() + deltay
        window.geometry(f"+{x}+{y}")

    label.bind('<ButtonPress-1>', start_move)
    label.bind('<ButtonRelease-1>', stop_move)
    label.bind('<B1-Motion>', on_move)

    return window

root = tk.Tk()
root.withdraw()  # Hide the root window

# Create two draggable labels
mono_window = make_label_window("MONO")
dots_window = make_label_window("DOTS")

root.mainloop()
