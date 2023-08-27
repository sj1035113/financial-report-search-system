import pdfplumber
import requests
from io import BytesIO

def extract_text_from_pdf_url(pdf_url, page_number):
    text = ""
    response = requests.get(pdf_url)
    if response.status_code == 200:
        pdf_bytes = BytesIO(response.content)
        with pdfplumber.open(pdf_bytes) as pdf:
            if 0 < page_number <= len(pdf.pages):
                page = pdf.pages[page_number - 1]
                text = page.extract_text()
    return text

# 指定 PDF 文件的網址和要抓取的頁數
pdf_url = "https://d1io3yog0oux5.cloudfront.net/_c4aeacfacfa6879b9b7b146a69673f70/cocacolacompany/news/2021-10-27_Coca_Cola_Reports_Continued_Momentum_and_Strong_1040.pdf"  # 請替換為 PDF 文件的實際網址
page_number = 13

# 抓取第 8 頁的文字
extracted_text = extract_text_from_pdf_url(pdf_url, page_number)

# 輸出抓取到的文字
print(extracted_text)
