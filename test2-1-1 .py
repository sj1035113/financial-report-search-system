import json
class person_info():
    def __init__(self, birthday, name, data_list, data_dict={}):
        self.birthday = birthday
        self.name = name
        self.data_list = data_list
        self.data_dict = data_dict

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

class find_person():
    def __init__(self, target_name, data_list):
        self.target_name= target_name
        self.data_list = data_list
    
    def FindByName(self):
        for data in self.data_list:
            if data.get('name') == self.target_name:
                print(data['birthday'])
                print(data['name'])
                
            
    

def main():
    name = input("輸入姓名")
    birthday = input("輸入生日")
    with open('test.json','r') as file:
        data_list = json.load(file)

    person = person_info(birthday, name, data_list)
    print(person.get_name())
    person.creat_newblock()
    person.transport_to_json()
    print(person.print_list())
    print("成功添加")

    target_name = input ("想要搜尋的人")
    find_person1 = find_person(target_name,data_list)
    find_person1.FindByName()
if __name__ =="__main__":
    main()