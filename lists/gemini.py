enter_numbers = []
print("Enter numbers separated by commas (e.g., 1,2,3):")

for i in range(5):
    num = int(input(f"Enter number {i + 1}: "))
    enter_numbers.append(num)

print("\nList of entered numbers:", enter_numbers)
