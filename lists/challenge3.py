numbers = []

for i in range(5):
    number = int(input(f"Enter a number {i + 1}: "))
    numbers.append(number)

total = 0

for number in numbers:
    total += number

average = total / len(numbers)

highest = max(numbers)
lowest = min(numbers)

print("Numbers entered:", numbers)
print("Total:", total)
print("Average number:", average)
print("Highest number:", highest)
print("Lowest number:", lowest)