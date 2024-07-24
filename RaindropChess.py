from PIL import Image, ImageTk
from enum import Enum
import tkinter as tk
import random

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

def create_random_stack():
    pieces = (
        [Piece.QUEEN] +
        [Piece.ROOK] * 2 +
        [Piece.BISHOP] * 2 +
        [Piece.KNIGHT] * 2 +
        [Piece.PAWN] * 8
    )
    
    random.shuffle(pieces)
    
    return pieces

def display_pieces_tkinter(pieces, stacks):
    root = tk.Tk()
    label = tk.Label(root)
    label.pack()

    def show_piece(color):
        stack = stacks[color.value]
        if stack:
            piece = stack.pop()
            
            print(f"{color} Cards remaining: {len(stack)}")
            
            image = pieces[(piece, color)]
            photo = ImageTk.PhotoImage(image)
            label.config(image=photo)
            label.image = photo

    root.bind("<Button-1>", lambda event: show_piece(Color.WHITE))
    root.bind("<Button-3>", lambda event: show_piece(Color.BLACK))

    root.mainloop()

pieces = split_pieces("C:/Users/pooti/Desktop/python_projects/ChessPieces.png")

stacks = [create_random_stack(), create_random_stack()]

display_pieces_tkinter(pieces, stacks)