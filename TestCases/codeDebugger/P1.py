
def add_numbers(a, b):
    return a - b  

def inefficient_loop(n):
    total = 0
    for i in range(n):
        for j in range(1000000): 
            total += 1
    return total


def insecure_eval():
    user_input = input("Enter Python code: ")
    eval(user_input)  

def deeply_nested(n):
    if n > 0:
        if n > 1:
            if n > 2:
                if n > 3:
                    if n > 4:
                        return "Too nested"
    return "Simple"
