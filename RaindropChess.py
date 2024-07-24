from PIL import Image
from enum import Enum

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

def split_image(image_path):
    image = Image.open(image_path)
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
pieces = split_image("C:/Users/pooti/Desktop/python_projects/ChessPieces.png") 
print(pieces)