from PIL import Image, ImageTk
from enum import Enum
import tkinter as tk

class Piece(Enum):
    KING = 0
    QUEEN = 1
    BISHOP = 2
    KNIGHT = 3
    ROOK = 4
    PAWN = 5
    
class Color(Enum):
    WHITE = 0
    BLACK = 1

def split_pieces(image_path):
    image = Image.open(image_path).convert("RGBA")
    sub_image_width = 132
    sub_image_height = 132
    columns = 6
    rows = 2
    
    piece_names = [Piece.KING, Piece.QUEEN, Piece.BISHOP, Piece.KNIGHT, Piece.ROOK, Piece.PAWN]
    colors = [Color.WHITE, Color.BLACK]
    
    pieces = {}

    for row in range(rows):
        for col in range(columns):
            left = col * sub_image_width
            upper = row * sub_image_height
            right = left + sub_image_width
            lower = upper + sub_image_height
            
            sub_image = image.crop((left, upper, right, lower))
            piece_name = piece_names[col]
            color = colors[row]
            pieces[(piece_name, color)] = sub_image
    
    return pieces

def display_pieces_tkinter(pieces):
    keys = list(pieces.keys())
    index = 0
    
    root = tk.Tk()
    label = tk.Label(root)
    label.pack()

    def show_image(idx):
        image = pieces[keys[idx]]
        photo = ImageTk.PhotoImage(image)
        label.config(image=photo)
        label.image = photo
        root.title(f"{keys[idx][1].name.capitalize()} {keys[idx][0].name.capitalize()}")

    def on_space(event):
        nonlocal index
        index = (index + 1) % len(keys)
        show_image(index)

    root.bind("<space>", on_space)
    show_image(index)
    root.mainloop()

pieces = split_pieces("C:/Users/pooti/Desktop/python_projects/ChessPieces.png")

display_pieces_tkinter(pieces)