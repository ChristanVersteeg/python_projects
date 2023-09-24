import tkinter as tk

def draw_grid(canvas, width, height, num_cells):
    """Draws a grid on a canvas given its width, height, and number of cells."""
    spacing_x = width / num_cells
    spacing_y = height / num_cells

    font = ("Arial", 25, "bold")
    # Add the "0" for both x and y axis
    canvas.create_text(5, height - 5, text="0", anchor="sw", fill='black', font=font)
    canvas.create_text(5 + width - 10, height - 5, text="5", anchor="se", fill='black', font=font)
    canvas.create_text(5, 20 - 13, text="5", anchor="nw", fill='black', font=font)  # Adjusted the 5's y-axis position further

    for i in range(1, num_cells):
        x_position = i * spacing_x
        y_position = i * spacing_y
        
        canvas.create_line(x_position, 0, x_position, height, fill='gray')
        canvas.create_line(0, y_position, width, y_position, fill='gray')

        # Add numbers next to lines - x axis numbers are placed at the bottom, y axis numbers at the left.
        canvas.create_text(x_position, height - 5, text=str(i), anchor="s", fill='black', font=font)
        canvas.create_text(5, height - y_position, text=str(i), anchor="w", fill='black', font=font)

def main():
    root = tk.Tk()
    root.title('5x5 Grid Overlay')

    # Set window dimensions
    width = 500
    height = 500

    root.geometry(f"{width}x{height}+1015+590")

    canvas = tk.Canvas(root, bg='white')
    canvas.pack(fill=tk.BOTH, expand=True)

    draw_grid(canvas, width, height, 5)  # 5x5 grid

    root.wm_attributes('-transparentcolor', 'white')  # Make white color transparent for the entire window

    root.mainloop()

if __name__ == "__main__":
    main()
