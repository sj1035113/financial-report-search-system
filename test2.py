import json

class person_info():
    def __init__(self, birthday, name, data_list):
        self.name = name
        self.birthday = birthday
        self.data_list = data_list

    def get_birthday(self):
        return self.birthday
    
    def get_name(self):
        return self.name
    
    def creat_newblock(self):
        data_dict = {
            'name': self.name,
            'birthday': self.birthday
        }
        self.data_list.append(data_dict)
    
    def transport_to_json(self):
        with open("test.json", 'w') as file:
            json.dump(self.data_list, file, indent=4)  # 使用 indent 參數使 JSON 文件格式化，便於閱讀
            file.write("\n")

def main():
    name = input("輸入姓名")
    birthday = input("輸入生日")
    with open('test.json', 'r') as file:
        data_list = json.load(file)
    
    # 創建 person_info 實例並操作
    person = person_info(birthday, name, data_list)
    person.creat_newblock()
    person.transport_to_json()
    
    print(data_list)
    print("成功結束")

if __name__ == "__main__":
    main()









