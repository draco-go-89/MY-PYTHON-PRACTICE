# Ask user for the number
num = int(input("Multiplication table of: "))

limit = int(input("Till " + str(num) + " x: "))   # Ask user for the range limit

# Print multiplication table up to that limit
for i in range(1, limit + 1):
    print(num, "x", i, "=", num * i)
