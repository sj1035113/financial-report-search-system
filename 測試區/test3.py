import pygsheets
sheet_name = 'TEST'
gc = pygsheets.authorize(service_file = r"C:\Users\sj103\Downloads\financial-report-396808-7cfeec8d9bd9.json")
sh = gc.open(sheet_name)
worksheet = sh.worksheet_by_title('sheet1')
data = worksheet.get_all_values()
list = ['hi', 'mother', 'fucker']
#worksheet.update_values('A1',[list],majordim='COLUMNS')
#worksheet.delete_cols(2, 2)
new_column_data = ["新列3", "新列2", "新列1"]
worksheet.insert_rows(3, values=new_column_data)
#worksheet_names = [worksheet.title for worksheet in sh.worksheets()]

# 輸出所有工作表名稱
#print("所有工作表名稱：")
#for name in worksheet_names:
#    print(name)
#worksheet.clear()






