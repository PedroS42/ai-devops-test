def divide_numbers(a, b):
    if b == 0:
        raise ZeroDivisionError("Cannot divide by zero")
    div_result = a / b
    return div_result

print(divide_numbers(10, 5))