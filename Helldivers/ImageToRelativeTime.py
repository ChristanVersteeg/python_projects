from datetime import datetime, timedelta
from io import BytesIO
from PIL import Image, ImageGrab, ImageEnhance, ImageFilter
from pyperclip import copy
from pytesseract import image_to_string
from re import match, IGNORECASE

def parse_to_minutes(time):
    total_minutes = None
    
    def check_format(regex, mult_x, mult_y):
        matched_format = match(regex, time, IGNORECASE)
        
        if not matched_format: return
        
        nonlocal total_minutes
        x, y = map(int, matched_format.groups())
        total_minutes = x * mult_x + y * mult_y
    
    check_format(r"(\d+)D (\d+)H", 1440, 60)
    check_format(r"(\d+)H (\d+)M", 60, 1)
    
    if total_minutes is None: 
        raise ValueError(f"Format is not recognized, given format: {time if time != '' else 'FORMAT YIELDED EMPTY STRING.'}Make sure the format is either (0D/d 0H/h) or (0H/h 0M/m) (0 can be any number, and no brackets).")
    else: return total_minutes

def image_to_timestamp():
    image = ImageGrab.grabclipboard()
    
    if image is None: raise ValueError("Clipboard did not have an image copied.")
    
    byte_array = BytesIO()
    image.save(byte_array, format='PNG')
    byte_array.seek(0)
    
    image = Image.open(byte_array)
    image_enhance = ImageEnhance.Contrast(image).enhance(2)
    image_filter = image_enhance.filter(ImageFilter.SHARPEN)
    image_gray_scale = image_filter.convert('L')
    image_black_white = image_gray_scale.point(lambda x: 0 if x < 128 else 255, '1')
    
    time = image_to_string(image_black_white, lang="eng", config='--psm 6')
    time = time.replace("O", "0")
    
    current_time = datetime.now()
    time_difference = timedelta(minutes=parse_to_minutes(time))
    future_time = current_time + time_difference
    timestamp = int(future_time.timestamp())
    
    formatted_time = f"<t:{timestamp}:R>"
    copy(formatted_time)
    print(f"Formatted timestamp copied to clipboard: {formatted_time}")
image_to_timestamp()