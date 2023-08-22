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
    def __init__(self, company_name):
        self.company_name = company_name


    def load_new_data(self ,exist_company = None):
        while True:
            comfirm_to_continue = True
            input_str = input("輸入公司名稱(大寫): ")
            for company in exist_company:
                if input_str == company:
                    print('ISSUE: 此公司已在資料庫內\n')
                    comfirm_to_continue = False
                    break
            if  re.fullmatch(r"\b[A-Z]+\b",input_str):
                self.company_name = input_str
                break
            else:
                print("ISSUE: 輸入錯誤")
        if comfirm_to_continue == True:
            while True:
                input_str = input("輸入目前第幾季: ")
                if  re.fullmatch(r"\d{2} Q\d" ,input_str):
                    self.quarter = input_str
                    break
                else:
                    print("ISSUE: 輸入錯誤(例如:23 Q2)")
        if comfirm_to_continue == True:
            self.tracked_data_group = self.assemble_data()
            self.Data_moved_from_main()


    def search_data_and_show_data(self):
        whether_find = False
        companies_list = self.put_data_to_main()
        if self.company_name == 'all':
            for data_dict in companies_list:
                print(f"公司名: {data_dict.get('name')}")
                print(f"季度: {data_dict.get('quarter')}")
                print(f"追蹤數據:{data_dict.get('tracked_data_group')}")
        else:
            for data_dict in companies_list:
                if data_dict.get('name') == self.company_name:  #data_list.get('公司名') == company_name:
                    print("confirm")
                    print(f"公司名: {data_dict.get('name')}")
                    print(f"季度: {data_dict.get('quarter')}")
                    print(f"追蹤數據:{data_dict.get('tracked_data_group')}")
                    whether_find = True
            if whether_find == False:
                print("此公司未在數據庫")  


    def change_data(self, mode):       #目前僅針對我們還沒傳入company_data.json的數據進行更改但我們應該是要針對裡面的數據進行更改(目前插在沒有把原資料刪除)
        list = []                      #上面的mode分為自動跟手動
        index = 0
        confirm_to_continue = True    #確認是否要繼續。因為可能會出現不滿足條件，所以不能繼續執行
        companies_list = self.put_data_to_main()    #將資料庫的資料傳入這個函式，尋找我們的目標公司
        for data_dict in companies_list:
                if data_dict.get('name') == self.company_name:

                    self.company_name = data_dict.get('name')
                    print(f'公司名:{self.company_name}')
                    self.quarter = data_dict.get('quarter')
                    print(f"季度:{self.quarter}")
                    self.tracked_data_group = data_dict.get('tracked_data_group')
                    print(f'追蹤資料:{self.tracked_data_group}')
                else:
                    index+=1
        list = [self.company_name, self.quarter, self.tracked_data_group]
        if mode == 'manual_mode': 
            if None in list:
                print("此公司未曾輸入過")
                confirm_to_continue = False
            else:
                print(f"\n公司名 :{self.company_name}\n季度:{self.quarter}\n追蹤數據:{self.tracked_data_group}")
                change_data = input("輸入更改數據: ")
                match change_data:
                    case"公司名":
                        while True:
                            input_str = input("輸入公司名稱(大寫): ")
                            if  re.fullmatch(r"\b[A-Z]+\b",input_str):
                                self.company_name = input_str
                                break
                            else:
                                print("ISSUE 輸入錯誤")
                    case"季度":
                        while True:
                            input_str = input("輸入目前第幾季: ")
                            if  re.fullmatch(r"\d{2} Q\d" ,input_str):
                                self.quarter = input_str
                                break
                            else:
                                print("ISSUE: 輸入錯誤(例如:23 Q2)")
                    case"追蹤數據":
                        self.tracked_data_group = self.assemble_data()
        if mode == 'Automatically change quarterly data':
            present_quarter_number = self.quarter[-1]
            present_year_number = self.quarter[:2]
            present_quarter_number = int(present_quarter_number)
            present_year_number = int(present_year_number)
            if present_quarter_number == 4:
                present_year_number += 1
                present_quarter_number = 1
                self.quarter = str(present_year_number)+' Q'+str(present_quarter_number)
            else:
                present_quarter_number = int(present_quarter_number)
                present_quarter_number += 1
                self.quarter = str(present_year_number)+' Q'+str(present_quarter_number)

        if confirm_to_continue == True:
            self.Data_moved_from_main(index)
               

    def return_quarter_info_and_tracked_data_group(self):  #向外傳
        with open(r"C:\Users\sj103\OneDrive\文件\finacial report\main\company_data.json") as file:
            all_companies_list = json.load(file)
            for data_dict in all_companies_list:
                if data_dict.get('name') == self.company_name:
                    return data_dict.get('quarter'),data_dict.get('tracked_data_group')
      

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
        with open (r"C:\Users\sj103\OneDrive\文件\finacial report\main\company_data.json", "r") as file:
            list = json.load(file)
            return list


    def Data_moved_from_main(self, del_index = None): #內部呼叫用
        list = [self.company_name, self.quarter, self.tracked_data_group]
        if None in list:
            print("\nISSUE: 缺少資料")

        else:
            print(f"\n公司名 :{self.company_name}\n季度:{self.quarter}\n追蹤數據:{self.tracked_data_group}")
            input_str = input("確認資料(輸入true or false): ")

        if input_str == "true":
            data_dict = {
                            "name" : self.company_name,
                            "quarter" : self.quarter,
                            "tracked_data_group" : self.tracked_data_group,
                            }
            data_list = []
            with open(r"C:\Users\sj103\OneDrive\文件\finacial report\main\company_data.json", "r") as file:
                data_list = json.load(file)
            if del_index != None:
                data_list.pop(del_index)   
                print(f'del:{del_index}')
                print('已刪除')
            data_list.append(data_dict)
            with open(r'C:\Users\sj103\OneDrive\文件\finacial report\main\company_data.json', "w") as file:
                json.dump(data_list, file, indent=4)
            self.company_name  = self.quarter = self.tracked_data_group = data_list = data_dict = list = None
        else:
            print("未加入，脫離!!!")
            return
    
    
    def clear_data(self):
        self.quarter = self.tracked_data_group = self.company_name = None


class data_about_json(about_json):
    include_info_list = []
    list_for_creation = []
    def __init__(self, company_name):
        self.company_name = company_name

    def get_list_for_creation(self):
        return self.list_for_creation
    
    
    def get_company_name(self):
        return self.company_name
        

    def put_data_to_main(self):
        company_file_name = self.company_name + r'.json'
        company_file_location = os.path.join(r'C:\Users\sj103\OneDrive\文件\finacial report\main\個別公司數據', company_file_name)
        if os.path.exists(company_file_location):
            print('公司存在')
        else :
            print("ISSUE: 公司不存在")
            return

        with open(company_file_location, 'r') as file:
            self.include_info_list = json.load(file)
            return self.include_info_list


    def creat_new_quarter_data(self, quarter):
        self.list_for_creation = [self.company_name, quarter]


    def assemble_data_and_append_to_list_for_creation(self, item, value):       #需要先用creat_new_quarter_data建立一個list，裡面包含季度資訊，此函式僅支援新建dict並把他放入list
        dict = {item : value}
        self.list_for_creation.append(dict)


    def Data_moved_from_main(self, sender_list):          #這邊的list是要準備送出程式的list,也就是包含所有資訊dict的list
        temporary_list = []
        company_file_name = self.company_name + r'.json'
        company_file_location = os.path.join(r'C:\Users\sj103\OneDrive\文件\finacial report\main\個別公司數據', company_file_name)
        if os.path.exists(company_file_location):
            print('檔案存在')
        else :
            print("檔案不存在")
            try:
                with open(company_file_location, 'w') as file:
                    init_list = []
                    json.dump(init_list, file)
                    print("檔案新增成功")
            except:
                print('檔案新增錯誤')
        with open(company_file_location, 'r') as file:
            temporary_list = json.load(file)
        with open(company_file_location, 'w') as file:
            temporary_list.append(sender_list)
            json.dump(temporary_list, file, indent=4)


    def show_data(self, mode, search_target = None):
        match mode:
            case "quarter":
                confirm_to_continue = None
                for single_quarter_list in self.include_info_list:
                    if single_quarter_list[1] == search_target:
                        for item in single_quarter_list[2:]:
                            for key, value in item.items():
                                print(f"{key}: {value}")
                                confirm_to_continue = True
                if confirm_to_continue != True:
                    print('ISSUE: 此季度未在資料庫')
            case 'item':
                for single_quarter_list in self.include_info_list:
                    for item in single_quarter_list:
                        if type(item) == dict:
                            if search_target in item.keys():
                                print(f"{single_quarter_list[1]}:{item[search_target]}")
            case 'all':
                for single_quarter_list in self.include_info_list:
                    print(f'{single_quarter_list}\n')
                


class SearchByPDF:
    pattern = None
    def __init__(self, file_location, item, table_name, row):
        self.file_location = file_location
        self.item = item
        self.table_name = table_name
        self.row = row

    def search(self):
        pdf = pdfplumber.open(self.file_location)
        for i in range(len(pdf.pages)):
            page = pdf.pages[i].extract_text()
            if self.table_name in page:  #確認我們要的報表
                pattern = self.creat_pattern()
                match = re.search(pattern, page)
                if match:   #如果有搜尋到我們要的pattern
                    #print(match.group(0))
                    numbers = re.findall(number_pattern, match.group(0))
                    #print(numbers)
                    for i in numbers:   #將一整列轉換成一組list 
                        numbers = [self.convert_to_number(num) for num in numbers]  
                        self.row = int(self.row)
                        self.row = self.row-1
                        #print(numbers)
                        return numbers[self.row] #return 我們要的值


    def creat_pattern(self):      #內部呼叫使用r"(?:\(?\d{1,3}(?:,\d{3})*(?:\.\d+)?\)?)?\s*\$"
        multible_number_pattern = r"(?:\$(?:\s)?)?(\d{1,3}(?:,\d{3})*(?:\.\d+)?)(?:\s*(\d+))?"
        self.pattern = f"{self.item}\s+{multible_number_pattern}"
        print(self.item)
        return self.pattern


    def convert_to_number(self, number_str):    #內部呼叫使用; 將字串轉換成list
        number_str = number_str.replace(",", "")  # Remove commas
        if "(" in number_str and ")" in number_str:  # Check if both parentheses are present
            number_str = "-" + number_str[1:-1]  # Add negative sign to the number inside parentheses
        elif "(" in number_str:  # Check if only opening parenthesis is present
            number_str = "-" + number_str[1:]  # Add negative sign to the number
        return float(number_str) if "." in number_str else int(number_str)
    
    

def main():
    while True:
        mode = input("1:有關公司基本資料\n2:個別公司資料管理\n3:載入新財報\n4:離開\n請輸入要使用的項目: ")
        match mode:
            case "1":
                company_name = None
                while True:
                    service = input("1:新增公司資訊\n2:改變公司資訊\n3:搜尋公司資訊\n4:顯示所有公司資訊\n請輸入要使用的服務: ")
                    if service == '2' or service == '3':
                        while True:
                            input_str = input("公司名稱(大寫):")
                            if  re.fullmatch(r"\b[A-Z]+\b",input_str):
                                company_name = input_str
                                break
                            else: 
                                print('ISSUE: 輸入錯誤')
                        break
                    elif service =='1':
                        company_name == 'default'
                        break
                    elif service == '4':
                        company_name = 'all' 
                        break
                    else:
                        print('ISSUE: 輸入錯誤')

                operate_company_essential_data = company_about_json(company_name)       #在這裡宣告而不適放在match裡沒關係，因為程式執行一次，結著就會跳出重新再宣告一個
                match service:
                    case "1":
                        list = []
                        all_list = operate_company_essential_data.put_data_to_main()
                        for item in all_list:
                            list.append(item['name'])
                        operate_company_essential_data.load_new_data(list)
                    case "2":
                        operate_company_essential_data.change_data ('manual_mode')
                    case "3":
                        operate_company_essential_data.search_data_and_show_data()  
                    case "4":
                        operate_company_essential_data.search_data_and_show_data()
            case '2':
                confirm_to_continue = None
                company_name = None
                service = input('1:查看季度資料\n2:查看特定數據過往資料\n3:查看所有數據\n請輸入要使用的服務:')
                while True:
                    input_str = input('想要查看哪一間公司(大寫): ')
                    if re.fullmatch(r'\b[A-Z]+\b',input_str):
                        company_name = input_str
                        break
                    else:
                        print('ISSUE: 輸入錯誤')
                with open(r"C:\Users\sj103\OneDrive\文件\finacial report\main\company_data.json", "r") as file:
                    tem_list = json.load(file)
                    for tem_dict in tem_list:
                        if tem_dict.get('name') == company_name:
                            confirm_to_continue = True
                if confirm_to_continue ==True:
                    watch_data = data_about_json(company_name)
                    watch_data.put_data_to_main()
                    match service:
                        case '1':
                            while True:
                                input_str = input('想要查看哪一季度資料: ')
                                if  re.fullmatch(r"\d{2} Q\d" ,input_str):
                                    quarter = input_str
                                    break
                                else:
                                    print('ISSUE: 輸入錯誤(例如:23 Q2)')
                            watch_data.show_data('quarter', quarter)        #前面那個為模式選擇後面為查看的季度
                        case '2':
                            item = input("想要查看哪一個項目: ")
                            watch_data.show_data('item', item)
                        case '3':
                            watch_data.show_data('all')
                else:
                    print('ISSUE: 此公司未在資料庫')


            case "3":
                while True:
                    input_str = input('要新增哪一間公司: ')
                    if re.fullmatch(r'\b[A-Z]+\b', input_str):
                        company_name = input_str
                        break
                    else:
                        print('ISSUE: 輸入錯誤')

                file_location  = input("請輸入檔案位置: ")
                file_location = fr'{file_location}'
                ComapanyAboutJson = company_about_json(company_name)
                DataAboutJson = data_about_json(company_name) 
                quarter, tracked_data_group = ComapanyAboutJson.return_quarter_info_and_tracked_data_group()
            

                DataAboutJson.creat_new_quarter_data(quarter)
                for index in range(len(tracked_data_group)):
                    searchPDF = SearchByPDF(file_location,tracked_data_group[index-1][0], tracked_data_group[index-1][1], tracked_data_group[index-1][2] )
                    value = searchPDF.search()
                    print(value)
                    DataAboutJson.assemble_data_and_append_to_list_for_creation(tracked_data_group[index-1][0], value)
                list = DataAboutJson.get_list_for_creation()
                print(list)
                DataAboutJson.Data_moved_from_main(list)
                while True:
                    tem_variable = input('是否季度自動加一(輸入yes or no): ') 
                    if tem_variable == 'yes':
                        ComapanyAboutJson.change_data('Automatically change quarterly data')
                        break
                    elif tem_variable == 'no':
                        break
                    else:
                        print('ISSUE: 輸入錯誤')
            case '4':
                break
            case _:
                print('ISSUE: 輸入錯誤')

if __name__ == '__main__':
    main()

    

    
    
    
