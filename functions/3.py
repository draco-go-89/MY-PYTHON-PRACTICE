# Instead of printing the result inside the function, we can return the result.
# return is important

def add(a, b):
    return a + b

result = add(10, 20)

print(result)

if result > 25:
    print("Big number!")