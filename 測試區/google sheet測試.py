import pygsheets
gc = pygsheets.authorize(service_file = r"C:\Users\sj103\Downloads\financial-report-396808-7cfeec8d9bd9.json")
key = "1Trp2jTsoUR97jOW9OerTNoUO1mcY77PAYlEX7Okj67w"
sheet = gc.open_by_key(key)
class operation_about_google_sheet():
    def __init__(self, company_name):
        self.company_name = company_name

    def creat_and_init_new_sheet(self, company_list, item_list):       
#創建新的工作表，company_list 是存放在json的資料，理論上兩者會相同，item_list是要放入new_sheet的item
        for tem_company_name in company_list:
            if tem_company_name == self.company_name:
                return
            else:
                whether_find = False
        if whether_find == False:
            new_worksheet = sheet.add_worksheet(self.company_name)
            new_worksheet.update_values('B1', [item_list])

    def load_new_quarter_data(self, data_list, quarter):    #載入新的(包含插入和附加)季度資料
        worksheet = sheet.worksheet_by_title('sheet1')
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
                address = f'A{index+3}'     #加2的原因是因為+1為index是由0開始算另外一個+1是因為第一列要給list使用
                print(address)
                worksheet.update_values(address, [data_list])
            else:
                worksheet.insert_rows(insert_index+2, values = data_list)       #插入第三行他會在第四行作用
                print(insert_index+2)       
            
    def change_item_data(self, item_list):    #更改新的項目資料
        worksheet = sheet.worksheet_by_title(self.company_name)
        worksheet.update_values('B1', [item_list])


item_list = ["eps", '全美門市數','全球門市數', 'TEST']
data_list = [2334, 87678, 242313]
company_list = ["KO",'SBUX','AMZN']
company_name = input("請輸入公司名稱: ")
OperationAboutGoogleSheet = operation_about_google_sheet(company_name)
OperationAboutGoogleSheet.creat_and_init_new_sheet(company_list, item_list)
OperationAboutGoogleSheet.load_new_quarter_data(data_list, "23 Q2")
OperationAboutGoogleSheet.change_item_data(item_list)








