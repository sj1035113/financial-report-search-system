import re
import os
import json
import pdfplumber
import pygsheets
import requests
from io import BytesIO

gc = pygsheets.authorize(service_file = r"C:\Users\sj103\Downloads\financial-report-396808-7cfeec8d9bd9.json")
key = "1ySSrFMaCFnUQHHWeOFy0ZkR4oHQD7hYgjDRqv8cODGs"
sheet = gc.open_by_key(key)
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
        comfirm_to_continue = True
        for company in exist_company:
            if self.company_name == company:
                print('ISSUE: 此公司已在資料庫內\n')
                comfirm_to_continue = False

        if comfirm_to_continue == True:
            while True:
                input_str = input("輸入目前第幾季: ")
                if  re.fullmatch(r"\d{2} Q\d" ,input_str):
                    self.quarter = input_str
                    break
                else:
                    print("ISSUE: 輸入錯誤(例如:23 Q2)")
        if comfirm_to_continue == True:
            self.tracked_data_group, item_list= self.assemble_data()
            self.Data_moved_from_main()
            return item_list


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
        list = []                      #上面的mode分為自動跟手動 自動模式是要再尋找完新的數據列的時候自動將弟度往後加一
        item_list = []
        index = 0
        change_item = None
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
                change_item = input("輸入更改數據: ")
                match change_item:
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
                        self.tracked_data_group, item_list = self.assemble_data()

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

        if confirm_to_continue == True:     #這邊直接回傳confirm_to_continue，因為他會直接決定googlesheet要不要繼續跑
            self.Data_moved_from_main(index)
            return item_list, confirm_to_continue, change_item
               

    def return_quarter_info_and_tracked_data_group(self):  #向外傳
        with open(r"C:\Users\sj103\OneDrive\文件\finacial report\main\company_data.json") as file:
            all_companies_list = json.load(file)
            for data_dict in all_companies_list:
                if data_dict.get('name') == self.company_name:
                    return data_dict.get('quarter'),data_dict.get('tracked_data_group')
      

    def assemble_data(self): #內部呼叫用
        count = 1
        data_group = []     #給json用
        item_list = []  #給google sheet用
        while True:
            try:
                single_data = []
                item = input(f"追蹤數據{count} (按crtl+c結束): ")
                single_data.append(item)
                single_data.append(input(f"{single_data[0]}屬於哪一個報表 (按crtl+c結束): "))
                single_data.append(input(f"{single_data[0]}位於{single_data[1]}第幾行 (按crtl+c結束): "))
                count += 1
                data_group.append(single_data)
                item_list.append(item)

            except KeyboardInterrupt:
                break
        return data_group, item_list
         
         
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


    def creat_new_quarter_data(self, quarter, url):
        self.list_for_creation = [self.company_name, quarter, url]


    def assemble_data_and_append_to_list_for_creation(self, item, value):       #需要先用creat_new_quarter_data建立一個list，裡面包含季度資訊，此函式僅支援新建dict並把他放入list
        dict = {item : value}
        self.list_for_creation.append(dict)


    def Data_moved_from_main(self, send_list):          #這邊的list是要準備送出程式的list,也就是包含所有資訊dict的list
        all_data_list = []
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
            all_data_list = json.load(file)
            try:                                                        #確認data_about_json裡面沒有相同的資料
                for index in range(len(all_data_list)):
                    if all_data_list[index][1] == send_list[1]:
                        del all_data_list[index]
                        break
            except IndexError:
                pass
        with open(company_file_location, 'w') as file:
            insert_index = self.insert_index(all_data_list, send_list[1])
            all_data_list.insert(insert_index, send_list)
            print(f"insert: {insert_index}")
            json.dump(all_data_list, file, indent=4)


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


    def insert_index(self, all_data_list, quarter):      #基本上是內部再用，用來決定要插入哪一個地方
        if not all_data_list :        #完全空的狀況下
            return 0
        else:
            index = 0
            insert_index = 0
            while True: 
                try:
                    print(all_data_list[index][1])
                    print(quarter)
                    present_collected_quarter = all_data_list[index][1]
                    present_year, present_quarter = present_collected_quarter.split(" ")
                    target_year, target_quarter = quarter.split(" ")
                    if target_year < present_year:
                        index += 1
                    elif target_year > present_year:
                        index += 1
                        insert_index = index
                    elif target_year == present_year:
                        if target_quarter > present_quarter:
                            index += 1
                            insert_index = index
                        elif target_quarter < present_quarter:
                            index += 1           
                except IndexError:
                    break

        return insert_index



class SearchByPDF:
    pattern = None
    def __init__(self, url, item, table_name, row):
        self.url = url
        self.item = item
        self.table_name = table_name
        self.row = row
        

    def search(self):

        #pdf_url = "https://d1io3yog0oux5.cloudfront.net/_b052a9abc81a1c2c95944f545dcbe4f2/cocacolacompany/db/734/7987/earnings_release/2023+Q1+Earnings+Release+%28Ex-99.1%29_Full+Release.pdf"
        response = requests.get(self.url) 
        pdf_data = response.content
        pdf = pdfplumber.open(BytesIO(pdf_data))
        for i in range(len(pdf.pages)):
            page = pdf.pages[i].extract_text()
            if self.table_name in page:  #確認我們要的報表
                pattern = self.creat_pattern()
                match = re.search(pattern, page)
                if match:   #如果有搜尋到我們要的pattern
                    print(match.group(0))
                    numbers = re.findall(number_pattern, match.group(0))
                    print(numbers)
                    for i in numbers:   #將一整列轉換成一組list 
                        numbers = [self.convert_to_number(num) for num in numbers]  
                        self.row = int(self.row)
                        self.row = self.row-1
                        #print(numbers)
                        return numbers[self.row] #return 我們要的值


    def creat_pattern(self):      #內部呼叫使用r"(?:\(?\d{1,3}(?:,\d{3})*(?:\.\d+)?\)?)?\s*\$"
        multible_number_pattern = r"(\$?\(?\s?(-?\d{1,3}(?:,\d{3})*(?:\.\d+)?)\)?\s*)+"
       #multible_number_pattern = r"((?:\(?\d{1,3}(?:,\d{3})*(?:\.\d+)?\)?)\s*)+"原pattern
        self.pattern = f"{self.item}\s*{multible_number_pattern}"
        print(self.item)
        return self.pattern


    def convert_to_number(self, number_str):    #內部呼叫使用; 將字串轉換成list
        number_str = number_str.replace(",", "")  # Remove commas
        if "(" in number_str and ")" in number_str:  # Check if both parentheses are present
            number_str = "-" + number_str[1:-1]  # Add negative sign to the number inside parentheses
        elif "(" in number_str:  # Check if only opening parenthesis is present
            number_str = "-" + number_str[1:]  # Add negative sign to the number
        return float(number_str) if "." in number_str else int(number_str)


class operation_about_google_sheet():
    def __init__(self, company_name):
        self.company_name = company_name


    def creat_and_init_new_sheet(self, company_list, item_list):       
#創建新的工作表，company_list 是存放在json的資料，理論上兩者會相同，item_list是要放入new_sheet的item
        whether_find = True
        for tem_company_name in company_list:
            if tem_company_name == self.company_name:
                return
            else:
                whether_find = False
        if whether_find == False:
            print("test")
            new_worksheet = sheet.add_worksheet(self.company_name)
            new_worksheet.update_values('B1', [item_list])


    def load_new_quarter_data(self, data_list, quarter):    #載入新的(包含插入和附加)季度資料
        worksheet = sheet.worksheet_by_title(self.company_name)
        quarter_list = []
        data_list.insert(0, quarter)
        quarter_index = 3
        while  True:        #生成quarter_list
            tem_list = ['A',str(quarter_index)]     #用來生成要尋找cell的位置
            address = ''.join(tem_list)
            quarter_data = worksheet.get_value(address)
            print(f"quarter_data: {quarter_data}")
            if quarter_data == '':
                break
            else:
                quarter_list.append(quarter_data)
                quarter_index += 1

        print(f"quarter_list = {quarter_list}")
        print(f"quarter: {quarter}")


        if not quarter_list :        #完全空的狀況下
            worksheet.insert_rows(2, values = data_list)
        else:
            index = 0
            insert_index = 0
            whether_update = False
            while True: 
                try:
                    present_collected_quarter = quarter_list[index]
                    present_year, present_quarter = present_collected_quarter.split(" ")
                    target_year, target_quarter = quarter.split(" ")
                    if target_year < present_year:
                        index += 1
                    elif target_year > present_year:
                        index += 1
                        insert_index = index
                        print(f"insert_index: {insert_index}")
                        print(f'quarter:{present_quarter}')
                    elif target_year == present_year:
                        if target_quarter > present_quarter:
                            index += 1
                            insert_index = index
                        elif target_quarter == present_quarter:
                            print('更新資料') 
                            whether_update = True
                            break
                        
                        elif target_quarter < present_quarter:
                            index += 1           
                except IndexError:
                    break
                
            if whether_update == True:
                address = f'A{index+3}'     #加3的原因是因為+1為index是由0開始算另外一個+1是因為第一列要給list使用+1要放中文名
                print(address)
                print(f"data_list = {data_list}")
                worksheet.update_values(address, [data_list])
            else:
                worksheet.insert_rows(insert_index+2, values = data_list)       #插入第三行他會在第四行作用
                print(insert_index+2)       

            
    def change_item_data(self, item_list):    #更改新的項目資料
        worksheet = sheet.worksheet_by_title(self.company_name)
        worksheet.update_values('B1', [item_list])


    def del_data(self ,row):        #刪除行
        worksheet = sheet.worksheet_by_title(self.company_name)
        worksheet.delete_rows(row)


    def clear_data(self, start_cell = None, end =None):        #清除整個列表
        worksheet = sheet.worksheet_by_title(self.company_name)
        worksheet.clear(start_cell)


    def update_row(self, row, data_list, col_offset = 0):
        worksheet = sheet.worksheet_by_title(self.company_name)
        worksheet.update_row(row, data_list, col_offset)

def main():
    while True:
        mode = input("1:有關公司基本資料\n2:個別公司資料管理\n3:載入新財報\n4:離開\n請輸入要使用的項目: ")
        match mode:
            case "1":
                company_name = None
                while True:
                    service = input("1:新增公司資訊\n2:改變公司資訊\n3:搜尋公司資訊\n4:顯示所有公司資訊\n5:離開\n請輸入要使用的服務: ")
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
                    elif service == '5':
                        break
                    else:
                        print('ISSUE: 輸入錯誤')
                match service:
                    case "1":
                        while True:
                            input_str = input("輸入公司名稱(大寫): ")
                            if  re.fullmatch(r"\b[A-Z]+\b",input_str):
                                company_name = input_str
                                break
                            else:
                                print("ISSUE: 輸入錯誤")
                        operate_company_essential_data = company_about_json(company_name)       
                        OperationAboutGoogleSheet = operation_about_google_sheet(company_name)
                        company_list = []
                        all_list = operate_company_essential_data.put_data_to_main()    #將已有的公司取出來並放入list中
                        for item in all_list:
                            company_list.append(item['name'])
                        item_list = operate_company_essential_data.load_new_data(company_list)
                        OperationAboutGoogleSheet.creat_and_init_new_sheet(company_list, item_list)

                    case "2":
                        operate_company_essential_data = company_about_json(company_name)
                        OperationAboutGoogleSheet = operation_about_google_sheet(company_name)
                        DataAboutJson = data_about_json(company_name)
                        item_list, confirm_to_continue, mode = operate_company_essential_data.change_data ('manual_mode')      #change_data包含了拿出來、更改、放回三大功能
                        if confirm_to_continue == True:
                            print(f"item_list = {item_list}")
                            OperationAboutGoogleSheet.change_item_data(item_list)
                        if mode == '追蹤數據':
                            while True:
                                answer = input("是否要根據新的追蹤數據更改數據(輸入yes or no):")
                                if answer == "yes" or answer == 'no':
                                    break
                                else :
                                    print ("輸入錯誤")
                            if answer == 'yes':
                                change_essential_data = company_about_json(company_name)
                                list_of_data_in_a_specific_company = DataAboutJson.put_data_to_main()
                                quarter, tracked_data_group = change_essential_data.return_quarter_info_and_tracked_data_group()
                                for quarter_index in range(len(list_of_data_in_a_specific_company)):
                                    url = list_of_data_in_a_specific_company[quarter_index][2]
                                    quarter = list_of_data_in_a_specific_company[quarter_index][1]
                                    DataAboutJson.creat_new_quarter_data(quarter, url)
                                    data_list = []
                                    for item_index in range(len(tracked_data_group)):
                                        searchPDF = SearchByPDF(url, tracked_data_group[item_index][0], tracked_data_group[item_index][1], tracked_data_group[item_index][2] )
                                        value = searchPDF.search()
                                        data_list.append(value)         #data_list 給google sheet用
                                        DataAboutJson.assemble_data_and_append_to_list_for_creation(tracked_data_group[item_index][0], value)
                                        dict_list = DataAboutJson.get_list_for_creation()       #dict_DiCt給json用
                                    DataAboutJson.Data_moved_from_main(dict_list)
                                    print(data_list)
                                    OperationAboutGoogleSheet.load_new_quarter_data(data_list, quarter)
                       
                            elif answer == 'no':
                                pass   
                                
                    case "3":
                        operate_company_essential_data = company_about_json(company_name)
                        operate_company_essential_data.search_data_and_show_data()  

                    case "4":
                        operate_company_essential_data = company_about_json(company_name)
                        operate_company_essential_data.search_data_and_show_data()

                    case '5':
                        pass
            
            
            case '2':
                confirm_to_continue = None
                company_name = None
                while True:
                    service = input('1:查看季度資料\n2:查看特定數據過往資料\n3:查看所有數據\n4:離開\n請輸入要使用的服務:')
                    if service == "1" or service == "2" or service == "3" or service == "4":
                        break
                    else:
                        print("ISSUE: 輸入錯誤")
                if service == '4':
                    pass
                elif service == '1' or service == '2' or service == '3':
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
                    service = input("1.往後新增新的資料\n2.更改或添加舊有資料\n3.連續更新季度\n4.離開\n請選擇服務: ")
                    if service == '1' or service == '2' or service == '3':
                        break
                    else:
                        print(" ISSUE: 輸入錯誤")
                        
                if service == '1' or service == '2':
                    while True:
                        input_str = input('要新增哪一間公司: ')
                        if re.fullmatch(r'\b[A-Z]+\b', input_str):
                            company_name = input_str
                            break
                        else:
                            print('ISSUE: 輸入錯誤')

                    data_list = []
                    url  = input("請輸入網址位置: ")
                    url = fr'{url}'
                    OperationAboutGoogleSheet = operation_about_google_sheet(company_name)                
                    ComapanyAboutJson = company_about_json(company_name)
                    DataAboutJson = data_about_json(company_name) 
                    quarter, tracked_data_group = ComapanyAboutJson.return_quarter_info_and_tracked_data_group()
                    if service == '2':
                        while True:
                                input_str = input("輸入目前第幾季: ")
                                if  re.fullmatch(r"\d{2} Q\d" ,input_str):
                                    quarter = input_str
                                    break
                                else:
                                    print("ISSUE: 輸入錯誤(例如:23 Q2)")

                    DataAboutJson.creat_new_quarter_data(quarter, url)
                    for index in range(len(tracked_data_group)):
                        searchPDF = SearchByPDF(url, tracked_data_group[index][0], tracked_data_group[index][1], tracked_data_group[index][2] )
                        value = searchPDF.search()      #value要傳出來並建立成一個list然後給google sheet
                        data_list.append(value)
                        DataAboutJson.assemble_data_and_append_to_list_for_creation(tracked_data_group[index][0], value)
                        dict_list = DataAboutJson.get_list_for_creation()
                    print(dict_list)
                    DataAboutJson.Data_moved_from_main(dict_list)
                    print('success')
                    OperationAboutGoogleSheet.load_new_quarter_data(data_list, quarter)


                    if service == '1':
                        while True:
                            tem_variable = input('是否季度自動加一(輸入yes or no): ') 
                            if tem_variable == 'yes':
                                ComapanyAboutJson.change_data('Automatically change quarterly data')
                                break
                            elif tem_variable == 'no':
                                break
                            else:
                                print('ISSUE: 輸入錯誤')
                
                elif service == '3':
                    start_qaurter_index = None
                    end_quarter_index = None
                    company_name = None
                    quarter_list = []
                    while True:
                        input_str = input('要新增哪一間公司: ')
                        if re.fullmatch(r'\b[A-Z]+\b', input_str):
                            company_name = input_str
                            break
                        else:
                            print('ISSUE: 輸入錯誤')
                    operate_company_essential_data = company_about_json(company_name)
                    OperationAboutGoogleSheet = operation_about_google_sheet(company_name)
                    DataAboutJson = data_about_json(company_name)

                    list_of_data_in_a_specific_company = DataAboutJson.put_data_to_main()
                    quarter, tracked_data_group = operate_company_essential_data.return_quarter_info_and_tracked_data_group()
                    quarter = None
                    for list in list_of_data_in_a_specific_company:     #獲取所有季度，有沒有這一行其實都沒差
                        quarter_list.append(list[1]) 
                    print(f"所有季度: {quarter_list}")
                    while  True:
                        input_str = input("要從哪一個季度開始(例:23 Q2): ")
                        whether_find = False
                        for quarter_index in range(len(quarter_list)):
                            if quarter_list[quarter_index] == input_str:
                                start_qaurter_index = quarter_index
                                whether_find = True
                        if whether_find == True:
                            break
                        else:
                            print("此季度未輸入過")

                    while  True:
                        input_str = input("哪一個季度結束(例:23 Q2): ")
                        whether_find = False
                        for quarter_index in range(len(quarter_list)):
                            if quarter_list[quarter_index] == input_str:
                                end_quarter_index = quarter_index
                                whether_find = True
                        if whether_find == True:
                            break
                        else:
                            print("此季度未輸入過")           
                    
                    for quarter_index in range(start_qaurter_index, end_quarter_index+1):
                        url = list_of_data_in_a_specific_company[quarter_index][2]
                        quarter = list_of_data_in_a_specific_company[quarter_index][1]
                        DataAboutJson.creat_new_quarter_data(quarter, url)
                        data_list = []
                        dict_list = []
                        for item_index in range(len(tracked_data_group)):
                            searchPDF = SearchByPDF(url, tracked_data_group[item_index][0], tracked_data_group[item_index][1], tracked_data_group[item_index][2] )
                            value = searchPDF.search()
                            data_list.append(value)         #data_list 給google sheet用
                            DataAboutJson.assemble_data_and_append_to_list_for_creation(tracked_data_group[item_index][0], value)
                            dict_list = DataAboutJson.get_list_for_creation()       #dict_list給json用
                        DataAboutJson.Data_moved_from_main(dict_list)
                        OperationAboutGoogleSheet.update_row(quarter_index+3, data_list, 1)
                
                elif service == '4':
                    pass
            
            
            case '4':
                break


            case _:
                print('ISSUE: 輸入錯誤')

if __name__ == '__main__':
    main()

    

    
    
    
