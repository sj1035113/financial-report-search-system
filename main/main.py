import re
import os
import json
import pdfplumber

number_pattern = r"\(?\d{1,3}(?:,\d{3})*(?:\.\d+)?\)?" 

class about_json():
    data = []     

    def show_data(self):
        pass

    def Data_moved_from_main(self):
        pass

    def put_data_to_main(self):
        pass


class company_about_json(about_json):
    quarter = None
    tracked_data_group = None
    company_name = None


    def load_new_data(self):
        while True:
            input_str = input("輸入公司名稱(大寫): ")
            if  re.fullmatch(r"\b[A-Z]+\b",input_str):
                company_name = input_str
                break
            else:
                print("輸入錯誤")

        while True:
            input_str = input("輸入目前第幾季: ")
            if  re.fullmatch(r"\d{2} Q\d" ,input_str):
                quarter = input_str
                break
            else:
                print("輸入錯誤(例如:23 Q2)")

        tracked_data_group = self.assemble_data()
        self.Data_moved_from_main(company_name, quarter, tracked_data_group)
        return self.company_name, self.quarter, self.tracked_data_group


    def search_data_and_show_data(self):
        company_name = input("輸入要尋找的公司(如果要全部顯示的話請輸入all):")
        all_companies_list = self.put_data_to_main()
        if company_name == 'all':
            for data_dict in all_companies_list:
                print(f"公司名: {data_dict.get('name')}")
                print(f"季度: {data_dict.get('quarter')}")
                print(f"追蹤數據:{data_dict.get('tracked_data_group')}")
        else:
            for data_dict in all_companies_list:
                if data_dict.get('name') == company_name:  #data_list.get('公司名') == company_name:
                    print("confirm")
                    print(f"公司名: {data_dict.get('name')}")
                    print(f"季度: {data_dict.get('quarter')}")
                    print(f"追蹤數據:{data_dict.get('tracked_data_group')}")        


    def change_data(self, company_name):       #目前僅針對我們還沒傳入company_data.json的數據進行更改但我們應該是要針對裡面的數據進行更改(目前插在沒有把原資料刪除)
        list = self.put_data_to_main()
        company_name, self.quarter, self.tracked_data_group = list 
        if None in list:
            print("尚未載入數據")
        else:
           print(f"\n公司名 :{self.company_name}\n季度:{self.quarter}\n追蹤數據:{self.tracked_data_group}")
           change_data = input("輸入更改數據: ")
           match change_data:
                case"公司名":
                   self.company_name = input("公司名: ")
                case"季度":
                    self.quarter = input("季度: ")
                case"追蹤數據":
                    self.tracked_data_group = self.assemble_data()
        self.Data_moved_from_main(company_name )            
        return [self.company_name, self.quarter, self.tracked_data_group]


    def return_tracked_data_group(self, company_name):  #向外傳
        with open('company_data.json') as file:
            all_companies_list = json.load(file)
            for data_dict in all_companies_list:
                if data_dict.get('name') == company_name:
                    return data_dict.get('tracked_data_group')
      

    def assemble_data(self): #內部呼叫用
        count = 1
        data_group = []
        while True:
            try:
                single_data = []
                single_data.append(input(f"追蹤數據{count} (按crtl+c結束): "))
                single_data.append(input(f"{single_data[0]}屬於哪一個報表 (按crtl+c結束): "))
                single_data.append(input(f"{single_data[0]}位於{single_data[1]}第幾行 (按crtl+c結束): "))
                count += 1
                data_group.append(single_data)

            except KeyboardInterrupt:
                break
        return data_group
         
         
    def put_data_to_main(self): #內部呼叫用
        with open ('company_data.json', "r") as file:
            list = json.load(file)
            return list


    def Data_moved_from_main(self, company_name, quarter, tracked_data_group):#內部呼叫用
        list = [company_name, quarter, tracked_data_group]
        if None in list:
            print("\nissue:缺少資料")

        else:
            print(f"\n公司名 :{company_name}\n季度:{quarter}\n追蹤數據:{tracked_data_group}")
            input_str = input("確認資料(輸入true or false): ")

        if input_str == "true":
            data_dict = {
                            "name" : company_name,
                            "quarter" : quarter,
                            "tracked_data_group" : tracked_data_group,
                            }
            data_list = []
            with open('company_data.json', "r") as file:
                data_list = json.load(file)   
            data_list.append(data_dict)
            with open('company_data.json', "w") as file:
                json.dump(data_list, file, indent=4)
            company_name  = quarter = tracked_data_group = data_list = data_dict = list = None
        else:
            print("脫離")
            return
    
    
    def clear_data(self):
        self.quarter = self.tracked_data_group = self.company_name = None


class data_about_json(about_json):
    list = []
    def __init__(self, company_name):
        self.company_name = company_name


    def get_company_name(self):
        return self.company_name
        

    def put_data_to_main(self):
        company_file_name = self.company_name + r'.json'
        company_file_location = os.path.join(r'C:\Users\sj103\OneDrive\文件\finacial report\main\個別公司數據', company_file_name)
        if os.path.exists(company_file_location):
            print('檔案存在')
        else :
            print("檔案不存在")
            try:
                with open(company_file_location, 'w') as file:
                    print("檔案新增成功")
            except:
                print('檔案新增錯誤')
        with open(company_file_location, 'r') as file:
            list = json.load(file)
            return list


    def creat_new_quarter_data(self, quarter):
        self.list = [self.company_name, quarter]


    def assemble_data(self, item, value):     #需要先用creat_new_quarter_data建立一個list，裡面包含季度資訊，此函式僅支援新建dict並把他放入list
        dict = {item : value}
        self.list.append(dict)


    def Data_moved_from_main(self, list):          #這邊的list是要準備送出程式的list,也就是包含所有資訊dict的list
        temporary_list = []
        company_file_name = self.company_name + r'.json'
        company_file_location = os.path.join(r'C:\Users\sj103\OneDrive\文件\finacial report\main\個別公司數據', company_file_name)
        if os.path.exists(company_file_location):
            print('檔案存在')
        else :
            print("檔案不存在")
            try:
                with open(company_file_location, 'w') as file:
                    print("檔案新增成功")
            except:
                print('檔案新增錯誤')
        with open(company_file_location, 'r') as file:
            temporary_list = json.load(file)
        with open(company_file_location, 'w') as file:
            temporary_list.append(list)
            json.dump(temporary_list, file, indent=4)


    def show_data(self):
        pass


class SearchByPDF:
    pattern = None
    
    def search(self, file_location, table_name, item, row):
        pdf = pdfplumber.open(file_location)
        for i in range(len(pdf.pages)):
            page = pdf.pages[i].extract_text()
            if table_name in page:  #確認我們要的報表
                pattern = self.creat_pattern(item)
                match = re.search(pattern, page)
                if match:   #如果有搜尋到我們要的pattern
                    #print(match.group(0))
                    numbers = re.findall(number_pattern, match.group(0))
                    #print(numbers)
                    for i in numbers:   #將一整列轉換成一組list 
                        #print(f"{i}")
                        numbers = [self.convert_to_number(num) for num in numbers] 
                        #print(numbers)  
                        return numbers[row] #return 我們要的值


    def creat_pattern(self, item):      #內部呼叫使用
        multible_number_pattern = r"((?:\(?\d{1,3}(?:,\d{3})*(?:\.\d+)?\)?)\s*)+"
        self.pattern = fr"{item}\s+{multible_number_pattern}"
        return self.pattern


    def convert_to_number(self, number_str):    #內部呼叫使用; 將字串轉換成list
        number_str = number_str.replace(",", "")  # Remove commas
        if "(" in number_str and ")" in number_str:  # Check if both parentheses are present
            number_str = "-" + number_str[1:-1]  # Add negative sign to the number inside parentheses
        elif "(" in number_str:  # Check if only opening parenthesis is present
            number_str = "-" + number_str[1:]  # Add negative sign to the number
        return float(number_str) if "." in number_str else int(number_str)
    
    

def main():
    mode = input("請輸入要")


if __name__ == '__main__':
    pdf = company_about_json()
    pdf.search_data_and_show_data()


    

    
    
    
