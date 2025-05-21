import re

json_text = """

"""

product_ids = re.findall(r'"product_id"\s*:\s*"([^"]+)"', json_text)

for product_id in product_ids:
    print(product_id)