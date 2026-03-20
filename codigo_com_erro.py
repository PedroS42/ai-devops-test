def divide_numbers(a: float, b: float) -> float:
    """Divide two numbers.

    Args:
        a (float): The dividend.
        b (float): The divisor.

    Returns:
        float: The quotient.

    Raises:
        TypeError: If either input is not a number.
        ZeroDivisionError: If the divisor is zero.
    """
    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
        raise TypeError(f"Invalid input types: a={type(a)}, b={type(b)}")
    if b == 0:
        raise ZeroDivisionError("Cannot divide by zero")
    div_result = a / b
    return div_result

try:
    print(divide_numbers(10, 0))
except ZeroDivisionError as e:
    print(f"Error: {e}")

print(divide_numbers(10, 0)) # Raises ZeroDivisionError