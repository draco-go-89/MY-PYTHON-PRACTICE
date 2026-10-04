# Ask user for a number
num = int(input("Multiplication table of: "))

# Print multiplication table for that number
for i in range(1, 11):
    print(num, "x", i, "=", num * i)
