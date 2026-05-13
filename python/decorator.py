
# -------------------------------
# A SIMPLE DECORATOR
# -------------------------------

def my_decorator(func):
    def wrapper(*args, **kwargs):
        print("Before function call")

        # 🔥 This line calls the original function
        result = func(*args, **kwargs)

        print("After function call")

        return result
    return wrapper


# -------------------------------
# A NORMAL FUNCTION
# -------------------------------

@my_decorator
def greet(name, age):
    print(f"Hello {name}, you are {age} years old")
    return "Done"


# -------------------------------
# RUN IT
# -------------------------------

output = greet("Hamza", 25)
print("Returned value:", output)
