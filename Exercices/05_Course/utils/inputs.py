def read_int(msg: str) -> int:
    while True:
        try:
            return int(input(msg))
        except ValueError:
            print("Invalid input")

def read_float(msg: str) -> float:
    while True:
        try:
            return float(input(msg))
        except ValueError:
            print("Invalid input")