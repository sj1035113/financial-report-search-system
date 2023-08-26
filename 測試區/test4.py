import pygsheets

# 設定您的 Google Sheets 資訊
spreadsheet_id = '1Trp2jTsoUR97jOW9OerTNoUO1mcY77PAYlEX7Okj67w'
new_worksheet_title = '新工作表'

# 連接到 Google Sheets
gc = pygsheets.authorize(service_file=r"C:\Users\sj103\Downloads\financial-report-396808-7cfeec8d9bd9.json")

# 開啟指定的試算表
sh = gc.open_by_key(spreadsheet_id)
worksheet1 = sh.worksheet_by_title('sheet1')

# 新增工作表
#worksheet = sh.add_worksheet(title=new_worksheet_title, rows=10, cols=5)
a = worksheet1.get_value('G5')
if a == None:
    print('a is none')
if a == '':
    print('a is 空格')
print(f'{a}jiwef')
print(type(a))










    