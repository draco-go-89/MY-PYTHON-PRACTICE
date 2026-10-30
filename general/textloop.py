filename = "count_output.txt"

# User inputs
start = int(input("Enter starting number: "))
end = int(input("Enter ending number: "))
message = input("Enter the message to repeat after each number: ")

# Generate the file
if start > end:
    print("Starting number cannot be greater than ending number.")
else:
    with open(filename, "w", encoding="utf-8") as file:
        for number in range(start, end + 1):
            file.write(f"{number}. {message}\n")

    print("\nGeneration completed!")
    print(f"Total lines: {end - start + 1:,}")
    print(f"File saved as: {filename}")
