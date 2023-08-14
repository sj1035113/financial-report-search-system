import json
import re

class about_data():
    data = []
    data_list = []
    data_dict = None
    def __init__ (self, json_name):      
        self.json_name =  json_name

    def show_data(self):
        pass

    def take_out_data(self):
        pass

    def put_data(self):
        pass

class company_about_json(about_data):
    quarter = None
    format = None
    company_json = None

    def load_new_data(self):
        while True:
            input_str = input("輸入公司名稱(大寫): ")
            if  re.fullmatch(r"\b[A-Z]+\b",input_str):
                self.company_name = input_str
                break
            else:
                print("輸入錯誤")
        while True:
            input_str = input("輸入目前第幾季: ")
            if  re.fullmatch(r"\d{2} Q\d" ,input_str):
                self.quarter = input_str
                break
            else:
                print("輸入錯誤(例如:23 Q2)")
        while True:
            input_str = input("財報資料型式(HTML or PDF): ")
            if input_str == 'HTML' or input_str == 'PDF':
                self.format = input_str
                self.asseble_data()
                break
            else:
                print("輸入錯誤(HTML or PDF):")

    def change_data(self):
        if None in [self.company_name, self.format, self.quarter, self.data]:
            print("尚未載入數據")
        else:
           print(f"\n公司名 :{self.company_name}\n財報格式 :{self.format}\n季度:{self.quarter}\n追蹤數據:{self.data}")
           change_data = input("輸入更改數據:")
           match change_data:
                case"公司名":
                   self.company_name = input("公司名:")
                case"財報格式":
                    self.format = input("財報格式")
                case"季度":
                    self.quarter = input("季度")
                case"追蹤數據":
                    self.asseble_data()
           
    def Data_moved_from_main(self):
        if None in [self.company_name, self.format, self.quarter, self.data]:
            print("\nissue:缺少資料")
            print(f"\n公司名 :{self.company_name}\n財報格式 :{self.format}\n季度:{self.quarter}\n追蹤數據:{self.data}")
            return
        else:
            print(f"\n公司名 :{self.company_name}\n財報格式 :{self.format}\n季度:{self.quarter}\n追蹤數據:{self.data}")
            input_str = input("確認資料(輸入true or false):")
        if input_str == "true":
            self.data_dict = {
                              "name" : self.company_name,
                              "format" : self.format,
                              "quarter" : self.quarter,
                              "data" : self.data,
                            }
            self.data_list.append(self.data_dict)
            with open(self.json_name, "w") as file:
                json.dump(self.data_dict, file)
            self.data_dict = self.company_name = self.format = self.quarter = self.data = self.data_list = None
        else:
            return
    
    def asseble_data(self):
        count = 1
        while True:
            try:
                user_input = input(f"感興趣的資料{count} (輸入exit或按crtl+c結束測): ")
                self.data.append(user_input)
                count += 1
                if user_input == 'exit':
                    break

            except KeyboardInterrupt:
                break
    
    def show_data(self):
        print(f"\n公司名: {self.company_name}\n財報格式: {self.format}\n季度: {self.quarter}\n追蹤數據: {self.data}")            
            
    def put_data_to_main(self):
        pass

def main():
    CompanyAboutJson1 = company_about_json("company_data.json")
    CompanyAboutJson1.load_new_data()
    
 
    print(CompanyAboutJson1.format)
if __name__ == '__main__':
    CompanyAboutJson1 = company_about_json("company_data.json")
    CompanyAboutJson1.load_new_data()
    CompanyAboutJson1.Data_moved_from_main()
    print(f"測試{CompanyAboutJson1.data_list}")



    

    
    
    
