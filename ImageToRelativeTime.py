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
    byte_array = BytesIO()
    
    image.save(byte_array, format='PNG')
    byte_array.seek(0)
    
    image = Image.open(byte_array)
    time = image_to_string(image, lang="eng")
    time = time.replace("O", "0")
    
    current_time = datetime.now()
    time_difference = timedelta(minutes=parse_to_minutes(time))
    future_time = current_time + time_difference
    timestamp = int(future_time.timestamp())
    
    formatted_time = f"<t:{timestamp}:R>"
    copy(formatted_time)
    print(f"Formatted timestamp copied to clipboard: {formatted_time}")
image_to_timestamp()