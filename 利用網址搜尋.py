import pdfplumber
import requests
from io import BytesIO

# 下載網絡上的 PDF 檔案
pdf_url = "https://d1io3yog0oux5.cloudfront.net/_b052a9abc81a1c2c95944f545dcbe4f2/cocacolacompany/db/734/7987/earnings_release/2023+Q1+Earnings+Release+%28Ex-99.1%29_Full+Release.pdf"
response = requests.get(pdf_url)
pdf_data = response.content

# 將下載的 PDF 數據轉換為 pdfplumber 可處理的對象
pdf = pdfplumber.open(BytesIO(pdf_data))

# 提取文本並進行處理
first_page = pdf.pages[1].extract_text()
print(first_page)

# 關閉 PDF 對象
pdf.close()



    

    
    
    


                    
