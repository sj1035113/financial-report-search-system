import json

## 讀取JSON檔
with open('test.json', 'r') as f:
  ## 轉成Python Dict
  python_dict = json.load(fp = f)
print("Python Dict: ", python_dict)
print("Type: ", type(python_dict))