import pygsheets
gc = pygsheets.authorize(service_file = r"C:\Users\sj103\Downloads\financial-report-396808-7cfeec8d9bd9.json")
key = "1Trp2jTsoUR97jOW9OerTNoUO1mcY77PAYlEX7Okj67w"
sheet = gc.open_by_key(key)

worksheet = sheet.worksheet_by_title("sheet1")
my_list = [10, 20, 30, 40]
worksheet.update_row(1, my_list, col_offset=1)