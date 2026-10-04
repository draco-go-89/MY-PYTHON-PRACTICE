def square(number):
    return number * number


def is_even(number):
    return number % 2 == 0


def calculate_total(numbers):
    total = 0

    for number in numbers:
        total = total + number

    return total


print(square(5))

print(is_even(10))
print(is_even(7))

print(calculate_total([10, 20, 30, 40]))