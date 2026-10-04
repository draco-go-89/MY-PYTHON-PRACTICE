number = int(input("Enter a number: "))

if number > 0:
    print("This number is positive.")
elif number < 0:
    print("This number is negative.")
else:
    print("This number is zero.")

if number % 2 == 0:
    print("And even number.")
else:
        print("And odd number.")