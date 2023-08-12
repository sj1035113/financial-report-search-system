data_list = [
    {"name": "Alice", "age": 25},
    {"name": "Bob", "age": 30},
    {"name": "Charlie", "age": 28}
]
for data in data_list:
    if data['name'] == 'Bob':
        print(data['age'])
        print(data['name'])
