import json

class FinancialReport:      #宣告財報模板
    def __init__(self, url, data, company_name):
        self.url = url
        self.company_name = company_name
        self.data = data 
    def import_to_google_sheet(self):
        pass

    def colect_data(self, data):
        pass

    def import_to_json(self, company_name):     #將數據決定存進哪一間公司的檔案所以需要compant_name
        pass

    def CompanyFinancialReportByPDF(self):
        pass

    def CompanyFinancialReportByHTML(self):
        pass

if __name__ == "__main__" :
    with open('ompany_data.json','r') as file
    input("輸入要尋找的公司")
 