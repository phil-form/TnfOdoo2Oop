def addition(a, b):
    return a + b

def division(a, b):
    if b == 0:
        raise ValueError("division by zero")
    return a / b

def is_even(a):
    return a % 2 == 0