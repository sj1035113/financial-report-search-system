import re

text = "North America 3,904 3,590 9 (39) 1,033 1,056 (2) 1,041 1,064 (2)"
pattern = r"North America\s+((?:\(?\d{1,3}(?:,\d{3})*(?:\.\d+)?\)?)\s*)+"

matches = re.search(pattern, text)

if matches:
    numbers_group = matches.group(1)
    numbers = re.findall(r"\(?\d{1,3}(?:,\d{3})*(?:\.\d+)?\)?", numbers_group)
    
    processed_numbers = []
    for num in numbers:
        num = num.replace("(", "").replace(")", "")  # Remove parentheses if present
        num = num.replace(",", "")  # Remove commas
        
        if "(" in num and ")" in num:  # Check if both parentheses are present
            num = "-" + num[1:-1]  # Add negative sign to the number inside parentheses
        elif "(" in num:  # Check if only opening parenthesis is present
            num = "-" + num[1:]  # Add negative sign to the number
        
        processed_numbers.append(float(num) if "." in num else int(num))
    
    print(processed_numbers)



