numbers_str = ['3,904', '3,590', '9', '1,033', '1,056', '(2)', '1,041', '1,064', '(2)']

def convert_to_number(number_str):
    number_str = number_str.replace(",", "")  # Remove commas
    if "(" in number_str and ")" in number_str:  # Check if both parentheses are present
        number_str = "-" + number_str[1:-1]  # Add negative sign to the number inside parentheses
    elif "(" in number_str:  # Check if only opening parenthesis is present
        number_str = "-" + number_str[1:]  # Add negative sign to the number
    return float(number_str) if "." in number_str else int(number_str)

numbers = [convert_to_number(num) for num in numbers_str]
print(numbers)
