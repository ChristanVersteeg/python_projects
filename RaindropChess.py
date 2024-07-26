from PIL import Image, ImageTk
from enum import Enum
import tkinter as tk
import random

RGBA = "RGBA"
PIECE_WIDTH = 132
PIECE_HEIGHT = 132
PIECE_SCALE = 5
PIECE_SCALED_WIDTH = PIECE_WIDTH * PIECE_SCALE
PIECE_SCALED_HEIGHT = PIECE_HEIGHT* PIECE_SCALE
JOKER = Image.open("C:/Users/pooti/Desktop/python_projects/Raindrop.png").convert(RGBA)
JOKER = JOKER.resize((PIECE_SCALED_WIDTH, PIECE_SCALED_HEIGHT), Image.LANCZOS)

class Piece(Enum):
    KING = 0
    QUEEN = 1
    BISHOP = 2
    KNIGHT = 3
    ROOK = 4
    PAWN = 5
    JOKER = 6
PIECES_LENGTH = len(Piece) - 1
    
class Color(Enum):
    WHITE = 0
    BLACK = 1
COLORS_LENGTH = len(Color)
    
def split_pieces(image_path):
    image = Image.open(image_path).convert(RGBA)

    pieces = {}

    for row in range(COLORS_LENGTH):
        pieces[(Piece.JOKER, list(Color)[row])] = JOKER
        for col in range(PIECES_LENGTH):
            left = col * PIECE_WIDTH
            upper = row * PIECE_HEIGHT
            right = left + PIECE_WIDTH
            lower = upper + PIECE_HEIGHT
            
            sub_image = image.crop((left, upper, right, lower))
            sub_image = sub_image.resize((PIECE_SCALED_WIDTH, PIECE_SCALED_HEIGHT), Image.LANCZOS)
            piece = list(Piece)[col]
            color = list(Color)[row]
            pieces[(piece, color)] = sub_image
    
    return pieces

def create_random_stack():
    pieces = (
        [Piece.KING] +
        [Piece.QUEEN] +
        [Piece.ROOK] * 2 +
        [Piece.BISHOP] * 2 +
        [Piece.KNIGHT] * 2 +
        [Piece.PAWN] * 8 +
        [Piece.JOKER] * 2
    )
    
    random.shuffle(pieces)
    
    return pieces

def display_pieces_tkinter(pieces, stacks):
    root = tk.Tk()
    label = tk.Label(root)
    label.pack()
    
    blank = ImageTk.PhotoImage(JOKER)
    label.config(image=blank)
    label.image = blank
    
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