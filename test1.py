import json
class person_info():
    def __init__(self, birthday, name,data_list,data_dict={}):
        self.name = name
        self.data_dict = data_dict
        self.birthday = birthday
        self.data_list = data_list

    def get_birthday(self):
        return self.birthday
    
    def get_name(self):
        return self.name
    
    def creat_newblock(self):
        self.data_dict = {
            'name' : self.name,
            'birthday' : self.birthday
        }
        return self.data_dict
    
    def transport_to_json(self):
        self.data_list.append(self.data_dict)
        with open("test.json",'w') as file:
            json.dump(self.data_list,file,indent=4)

    def print_list(self):
        if self.data_list:
            print("data_list")
        else:
            print("尚未獲取資料")
            
    

def main():
    name = input("輸入姓名")
    birthday = input("輸入生日")
    with open('test.json','r') as file:
        data_list = json.load(file)

    person = person_info(name, birthday,data_list)
    person.creat_newblock()
    person.transport_to_json()
    print(person.print_list())
    print("成功結束")

if __name__ =="__main__":
    main()