import re
import os
from decimal import Decimal
from typing import List
from PyPDF2 import PdfReader

def extract_totaal_kosten_from_pdf(file_path: str) -> List[Decimal]:
    reader = PdfReader(file_path)
    kosten = []
    pattern = re.compile(r"Totaal kosten (BTW vrijgesteld)\s*([\d.,]+)")

    for page in reader.pages:
        text = page.extract_text()
        if not text:
            continue
        matches = pattern.findall(text)
        for match in matches:
            cleaned = match.replace('.', '').replace(',', '.')
            kosten.append(Decimal(cleaned))
    return kosten

def sum_totaal_kosten_in_folder(folder_path: str) -> Decimal:
    total = Decimal('0')
    for filename in os.listdir(folder_path):
        if filename.lower().endswith('.pdf'):
            file_path = os.path.join(folder_path, filename)
            kosten = extract_totaal_kosten_from_pdf(file_path)
            total += sum(kosten)
    return total

if __name__ == "__main__":
    folder = "D:\\Users\\python_projects"
    total_kosten = sum_totaal_kosten_in_folder(folder)
    print(f"Total 'Totaal kosten' sum: € {total_kosten:.2f}")
