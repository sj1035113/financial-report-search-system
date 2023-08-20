import json
import re

class about_data():
    data = []     

    def show_data(self):
        pass

    def Data_moved_from_main(self):
        pass

    def put_data_to_main(self):
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
                break
            else:
                print("輸入錯誤(HTML or PDF): ")
        self.data = self.assemble_data(self.data)
        return self.company_name, self.format, self.quarter, self.data 

    
    def change_data(self, list):
        if None in list:
            print("尚未載入數據")
            self.company_name, self.format, self.quarter, self.data = list
        else:
           print(f"\n公司名 :{self.company_name}\n財報格式 :{self.format}\n季度:{self.quarter}\n追蹤數據:{self.data}")
           change_data = input("輸入更改數據: ")
           match change_data:
                case"公司名":
                   self.company_name = input("公司名: ")
                case"財報格式":
                    self.format = input("財報格式: ")
                case"季度":
                    self.quarter = input("季度: ")
                case"追蹤數據":
                    self.data = self.assemble_data(self.data)
        return [self.company_name, self.format, self.quarter, self.data]
    
           
    def Data_moved_from_main(self, list, json_name):
        if None in list:
            self.company_name, self.format, self.quarter, self.data = list
            print("\nissue:缺少資料")
            return list
        else:
            print(f"\n公司名 :{self.company_name}\n財報格式 :{self.format}\n季度:{self.quarter}\n追蹤數據:{self.data}")
            input_str = input("確認資料(輸入true or false): ")

        if input_str == "true":
            data_dict = {
                              "name" : self.company_name,
                              "format" : self.format,
                              "quarter" : self.quarter,
                              "data" : self.data,
                            }
            data_list = []
            with open(json_name, "r") as file:
                data_list = json.load(file)   
            data_list.append(data_dict)
            with open(json_name, "w") as file:
                json.dump(data_list, file, indent=4)
            data_dict = self.company_name = self.format = self.quarter = self.data = data_list = list = None
        else:
            return
    
    
    def assemble_data(self, data): #內部呼叫用
        count = 1
        data = []
        while True:
            try:
                user_input = input(f"感興趣的資料{count} (輸入exit或按crtl+c結束): ")
                data.append(user_input)
                count += 1
                if user_input == 'exit':
                    break

            except KeyboardInterrupt:
                break
        return data
    

    def show_data(self, list):
        self.company_name, self.format, self.quarter, self.data = list
        print(f"\n公司名: {self.company_name}\n財報格式: {self.format}\n季度: {self.quarter}\n追蹤數據: {self.data}")            


    def put_data_to_main(self, json_name):
        with open (json_name, "r") as file:
            list = json.load(file)
            return list


    def search_data(self, all_companies_list, company_name):
        for data_dict in all_companies_list:
            if data_dict.get('name') == company_name:
                print(data_dict['birthday'])
                print(data_dict['name'])


def main():
    CompanyAboutJson1 = company_about_json("company_data.json")
    CompanyAboutJson1.load_new_data()
    print(CompanyAboutJson1.format)


if __name__ == '__main__':
    CompanyAboutJson = company_about_json()
    all_companies_list = CompanyAboutJson.put_data_to_main("company_data.json")
    print(all_companies_list)
    



    

    
    
    
