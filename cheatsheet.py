import tkinter as tk

def draw_grid(canvas, width, height, num_cells):
    """Draws a grid on a canvas given its width, height, and number of cells."""
    spacing_x = width / num_cells
    spacing_y = height / num_cells
    for i in range(1, num_cells):
        canvas.create_line(i * spacing_x, 0, i * spacing_x, height, fill='gray')
    for i in range(1, num_cells):
        canvas.create_line(0, i * spacing_y, width, i * spacing_y, fill='gray')

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
