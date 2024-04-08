from datetime import datetime, timedelta
from io import BytesIO
from PIL import Image
from PIL import ImageGrab
from pyperclip import copy
from pytesseract import image_to_string
from re import match

def parse_to_minutes(time):
    total_minutes = None
    
    def check_format(regex, mult_x, mult_y):
        matched_format = match(regex, time)
        
        if not matched_format: return
        
        nonlocal total_minutes
        x, y = map(int, matched_format.groups())
        total_minutes = x * mult_x + y * mult_y
    
    check_format(r"(\d+)D (\d+)H", 1440, 60)
    check_format(r"(\d+)H (\d+)M", 60, 1)
    
    if total_minutes is None: raise ValueError("Time format is not recognized.")
    else: return total_minutes

def image_to_timestamp():
    image = ImageGrab.grabclipboard()
    img_byte_arr = BytesIO()
    
    image.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)
    
    image = Image.open(img_byte_arr)
    text = image_to_string(image, lang="eng")
    
    total_minutes = parse_to_minutes(text)
    future_time = datetime.now() + timedelta(minutes=total_minutes)
    timestamp = int(future_time.timestamp())
    
    formatted_time = f"<t:{timestamp}:R>"
    copy(formatted_time)
    print(f"Formatted timestamp copied to clipboard: {formatted_time}")
image_to_timestamp()