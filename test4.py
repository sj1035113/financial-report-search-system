import pdfplumber
import re

def convert_to_number(number_str):
    number_str = number_str.replace(",", "")  # Remove commas
    if "(" in number_str and ")" in number_str:  # Check if both parentheses are present
        number_str = "-" + number_str[1:-1]  # Add negative sign to the number inside parentheses
    elif "(" in number_str:  # Check if only opening parenthesis is present
        number_str = "-" + number_str[1:]  # Add negative sign to the number
    return float(number_str) if "." in number_str else int(number_str)

table_name = "Operating Segments and Corporate"         #input("請輸入表格名稱: ")    #Operating Segments and Corporate 
region =  "North America"                               #input("追蹤地區: ")
pattern = r"North America\s+((?:\(?\d{1,3}(?:,\d{3})*(?:\.\d+)?\)?)\s*)+"# r"\s+(\d{1,3}(?:,\d{3})*(?:\.\d+)?\s+)+"
number_pattern = r"\(?\d{1,3}(?:,\d{3})*(?:\.\d+)?\)?"  # Updated pattern to capture numbers with or without parentheses


pdf = pdfplumber.open(r"C:\Users\sj103\Downloads\2023 Q1 Earnings Release (Ex-99.1)_Full Release.pdf")

for i in range(len(pdf.pages)):
    page = pdf.pages[i].extract_text()
    if table_name in page:
        match = re.search(pattern, page)
        print ("test2")
        if match: 
            print(match.group(0))
            numbers = re.findall(number_pattern, match.group(0))
            print(numbers)
            for i in numbers:
                print(f"{i}")
            numbers = [convert_to_number(num) for num in numbers] 
            print(numbers)   
                

 
pdf.close()







    