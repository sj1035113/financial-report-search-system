count= 0
data = []
while True:
    try:
        user_input = input(f"感興趣的資料{count} (輸入exit或按crtl+c結束測): ")
        data.append(user_input)
        count += 1
        if user_input == 'exit':
            break

    except KeyboardInterrupt:
            break
print(f"追蹤數據: {data}")


