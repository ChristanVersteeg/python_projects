import PyPDF2
import os
import re

def extract_numbers_from_text(text):
    """
    Extracts all euro amounts from a string and returns their sum.
    Handles negative numbers and spaces after the € symbol.
    """
    # Use regex to find all numbers prefixed with € (possibly having spaces in between)
    numbers = re.findall(r'€\s*-?\d+(?:\.\d+)?', text)
    # Extract just the numeric portion from each match and sum up the values
    return sum(float(re.search(r'-?\d+(?:\.\d+)?', num).group()) for num in numbers)

def sum_numbers_in_pdfs(folder_path):
    """
    Sums all the numbers from all PDFs in the given folder.
    """
    total_sum = 0

    # Iterate over all files in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith('.pdf'):
            print(f"Processing {filename}...")
            pdf_path = os.path.join(folder_path, filename)
            
            with open(pdf_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)  # Change is here
                
                # Iterate through all pages in the PDF
                for page_num in range(len(reader.pages)):
                    page = reader.pages[page_num]
                    text = page.extract_text()
                    print(extract_numbers_from_text(text))
                    total_sum += extract_numbers_from_text(text)
    
    return total_sum

result = sum_numbers_in_pdfs(r"D:\Users\Christan\Downloads\Invoices")
print(f"Total sum of numbers in all PDFs: {result}")
